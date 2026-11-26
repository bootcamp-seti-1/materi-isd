import os
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import aturan
from main import app

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_SQL = BASE_DIR / "db" / "schema.sql"
SEED_SQL = BASE_DIR / "db" / "seed.sql"


def _load_env_file() -> dict[str, str]:
    env_vars: dict[str, str] = {}
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, val = stripped.split("=", 1)
            env_vars[key.strip()] = val.strip().strip('"').strip("'")
    for k, v in os.environ.items():
        env_vars[k] = v
    return env_vars


def reset_database() -> None:
    cfg = _load_env_file()
    host = cfg.get("DB_HOST", "127.0.0.1")
    port = cfg.get("DB_PORT", "3306")
    user = cfg.get("DB_USER") or cfg.get("MYSQL_USER")
    password = cfg.get("DB_PASSWORD") or cfg.get("MYSQL_PASSWORD", "")
    db_name = cfg.get("DB_NAME") or cfg.get("MYSQL_DATABASE")

    assert user and db_name, (
        "Set DB_USER and DB_NAME (and DB_PASSWORD / DB_HOST / DB_PORT) in .env or environment."
    )

    base_cmd = ["mysql", f"-h{host}", f"-P{port}", f"-u{user}"]
    run_env = os.environ.copy()
    if password:
        run_env["MYSQL_PWD"] = password

    for sql_file in (SCHEMA_SQL, SEED_SQL):
        assert sql_file.exists(), f"Missing SQL file: {sql_file}"
        with sql_file.open("rb") as fh:
            result = subprocess.run(
                [*base_cmd, db_name],
                stdin=fh,
                capture_output=True,
                text=True,
                env=run_env,
            )
        if result.returncode != 0:
            pytest.fail(f"Failed running {sql_file.name}: {result.stderr.strip()}")


@pytest.fixture(autouse=True)
def fresh_db():
    reset_database()
    yield


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def require_implemented(resp, *, feature: str = "Endpoint") -> None:
    if resp.status_code == 501:
        pytest.skip(f"{feature} not implemented yet (501)")


# ---------- Extra unknown fields (422) ----------


def test_extra_fields_rejected_422(client: TestClient):
    r_menu = client.post(
        "/v1/menus",
        json={
            "name": "Es Cincau",
            "category": "minuman",
            "price": 5000,
            "stock": 10,
            "unknown_field": "nope",
        },
    )
    require_implemented(r_menu, feature="POST /v1/menus")
    assert r_menu.status_code == 422

    r_patch = client.patch(
        "/v1/menus/1",
        json={"price": 12000, "extra_key": 123},
    )
    require_implemented(r_patch, feature="PATCH /v1/menus/{menu_id}")
    assert r_patch.status_code == 422

    r_order = client.post(
        "/v1/orders",
        json={"menu_id": 1, "qty": 1, "hack": True},
    )
    require_implemented(r_order, feature="POST /v1/orders")
    assert r_order.status_code == 422


# ---------- Schema boundaries from aturan.py ----------


def test_menu_name_and_stock_boundaries(client: TestClient):
    min_name = "A" * aturan.NAMA_MIN
    max_name = "B" * aturan.NAMA_MAX

    r_min = client.post(
        "/v1/menus",
        json={"name": min_name, "category": "makanan", "price": aturan.HARGA_MIN, "stock": 0},
    )
    require_implemented(r_min, feature="POST /v1/menus")
    assert r_min.status_code == 201
    assert r_min.json()["stock"] == 0

    r_max = client.post(
        "/v1/menus",
        json={"name": max_name, "category": "minuman", "price": aturan.HARGA_MAX, "stock": aturan.STOK_MAX},
    )
    assert r_max.status_code == 201
    assert r_max.json()["stock"] == aturan.STOK_MAX

    # Over max name length -> 422
    r_too_long = client.post(
        "/v1/menus",
        json={"name": "C" * (aturan.NAMA_MAX + 1), "category": "makanan", "price": aturan.HARGA_MIN},
    )
    assert r_too_long.status_code == 422

    # Over max stock -> 422
    r_over_stock = client.post(
        "/v1/menus",
        json={"name": "Stok Berlebih", "category": "makanan", "price": aturan.HARGA_MIN, "stock": aturan.STOK_MAX + 1},
    )
    assert r_over_stock.status_code == 422


def test_order_qty_and_menu_id_boundaries(client: TestClient):
    for bad_payload in [
        {"menu_id": 0, "qty": 1},
        {"menu_id": -2, "qty": 1},
        {"menu_id": 1, "qty": aturan.QTY_MIN - 1},
        {"menu_id": 1, "qty": aturan.QTY_MAX + 1},
    ]:
        resp = client.post("/v1/orders", json=bad_payload)
        require_implemented(resp, feature="POST /v1/orders")
        assert resp.status_code == 422


# ---------- PATCH self-name & empty payload ----------


def test_patch_self_name_and_empty_body(client: TestClient):
    # Updating menu 1 with its own name (different casing) should NOT trigger 409
    r_self = client.patch("/v1/menus/1", json={"name": "nasi goreng"})
    require_implemented(r_self, feature="PATCH /v1/menus/{menu_id}")
    assert r_self.status_code == 200
    assert r_self.json()["name"] == "nasi goreng"

    # Empty JSON body on existing menu should return 200 without error
    r_empty = client.patch("/v1/menus/1", json={})
    assert r_empty.status_code == 200


# ---------- Order failure leaves stock untouched & discount threshold ----------


def test_failed_order_keeps_stock_and_discount_threshold(client: TestClient):
    before_stock = client.get("/v1/menus/3").json()["stock"]  # Roti Bakar: price=8000, stock=0
    qty_to_try = min(aturan.QTY_MAX, before_stock + 1)  # 1, within QTY_MIN..QTY_MAX

    # 409 insufficient stock should not change stock
    r_fail = client.post("/v1/orders", json={"menu_id": 3, "qty": qty_to_try})
    require_implemented(r_fail, feature="POST /v1/orders")
    assert r_fail.status_code == 409
    assert r_fail.json().get("detail") == "Stok tidak cukup"
    assert client.get("/v1/menus/3").json()["stock"] == before_stock

    # Exact BATAS_DISKON (e.g. Mi Ayam id=2: 5 * 10000 = 50000) gets discount
    r_exact = client.post("/v1/orders", json={"menu_id": 2, "qty": 5})
    assert r_exact.status_code == 201
    subtotal = 10000 * 5
    expected_total = (
        subtotal * (100 - aturan.DISKON_PERSEN) // 100
        if subtotal >= aturan.BATAS_DISKON
        else subtotal
    )
    assert r_exact.json()["total"] == expected_total


# ---------- Bonus list filtering, ordering, and laporan ----------


def test_bonus_filter_order_and_laporan_excludes_batal(client: TestClient):
    o1 = client.post("/v1/orders", json={"menu_id": 4, "qty": 2})  # Es Teh: 2 * 3000 = 6000
    require_implemented(o1, feature="POST /v1/orders")
    assert o1.status_code == 201

    o2 = client.post("/v1/orders", json={"menu_id": 6, "qty": 3})  # Air Mineral: 3 * 4000 = 12000
    assert o2.status_code == 201

    id1 = o1.json()["id"]
    id2 = o2.json()["id"]

    cancel_r = client.post(f"/v1/orders/{id1}/batal")
    require_implemented(cancel_r, feature="POST /v1/orders/{order_id}/batal")
    assert cancel_r.status_code == 200

    all_orders = client.get("/v1/orders")
    require_implemented(all_orders, feature="GET /v1/orders")
    assert all_orders.status_code == 200
    ids = [row["id"] for row in all_orders.json()]
    assert ids == sorted(ids) and len(ids) == 2

    only_baru = client.get("/v1/orders?status=baru")
    assert only_baru.status_code == 200
    assert [row["id"] for row in only_baru.json()] == [id2]

    only_batal = client.get("/v1/orders?status=batal")
    assert only_batal.status_code == 200
    assert [row["id"] for row in only_batal.json()] == [id1]

    laporan_resp = client.get("/v1/laporan")
    require_implemented(laporan_resp, feature="GET /v1/laporan")
    assert laporan_resp.status_code == 200
    assert laporan_resp.json() == {
        "jumlah_pesanan": 1,
        "pendapatan": o2.json()["total"],
    }
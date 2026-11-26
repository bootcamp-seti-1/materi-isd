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


# ---------- Seeded GET checks ----------


def test_get_menus_seeded(client: TestClient):
    resp = client.get("/v1/menus")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 6
    assert data[0]["name"] == "Nasi Goreng"


def test_get_menu_detail_not_found(client: TestClient):
    resp = client.get("/v1/menus/99999")
    assert resp.status_code == 404


# ---------- POST /v1/menus checks ----------


def test_post_menu_validation_422(client: TestClient):
    resp = client.post("/v1/menus", json={"name": "  ab  ", "category": "makanan", "price": 1000, "stock": 5})
    require_implemented(resp, feature="POST /v1/menus")
    assert resp.status_code == 422

    resp_step = client.post(
        "/v1/menus",
        json={
            "name": "Bakso Sapi",
            "category": "makanan",
            "price": aturan.HARGA_MIN + (aturan.KELIPATAN_HARGA // 2) if aturan.KELIPATAN_HARGA > 1 else -1,
            "stock": 5,
        },
    )
    assert resp_step.status_code == 422


def test_post_menu_create_and_duplicate_409(client: TestClient):
    payload = {
        "name": "  Soto Ayam  ",
        "category": "makanan",
        "price": 10000,
        "stock": 10,
    }
    resp = client.post("/v1/menus", json=payload)
    require_implemented(resp, feature="POST /v1/menus")
    assert resp.status_code == 201
    created = resp.json()
    assert created["name"] == "Soto Ayam"
    assert created["stock"] == 10

    dup = client.post(
        "/v1/menus",
        json={"name": "soto ayam", "category": "makanan", "price": 10000, "stock": 5},
    )
    assert dup.status_code == 409
    assert dup.json().get("detail") == "Nama menu sudah ada"


# ---------- PATCH /v1/menus/{menu_id} checks ----------


def test_patch_menu_order_404_422_409_200(client: TestClient):
    # 1. Missing menu -> 404
    r_404 = client.patch("/v1/menus/99999", json={"price": 15000})
    require_implemented(r_404, feature="PATCH /v1/menus/{menu_id}")
    assert r_404.status_code == 404

    # 2. Explicit null -> 422
    r_422 = client.patch("/v1/menus/1", json={"name": None})
    assert r_422.status_code == 422

    # 3. Duplicate name against another menu -> 409
    r_409 = client.patch("/v1/menus/1", json={"name": "mi ayam"})
    assert r_409.status_code == 409
    assert r_409.json().get("detail") == "Nama menu sudah ada"

    # 4. Partial update -> 200
    r_200 = client.patch("/v1/menus/1", json={"price": 14000})
    assert r_200.status_code == 200
    assert r_200.json()["price"] == 14000
    assert r_200.json()["name"] == "Nasi Goreng"


# ---------- POST /v1/orders checks ----------


def test_post_order_400_409_and_discount_201(client: TestClient):
    # 1. Menu not found -> 400
    r_400 = client.post("/v1/orders", json={"menu_id": 99999, "qty": 1})
    require_implemented(r_400, feature="POST /v1/orders")
    assert r_400.status_code == 400
    assert r_400.json().get("detail") == "Menu tidak ditemukan"

    # 2. Insufficient stock -> 409 (Roti Bakar id=3 has stock=0)
    r_409 = client.post("/v1/orders", json={"menu_id": 3, "qty": 1})
    assert r_409.status_code == 409
    assert r_409.json().get("detail") == "Stok tidak cukup"

    # 3. Valid order with discount threshold (Nasi Goreng id=1, price=12000, qty=5 -> subtotal 60000)
    r_201 = client.post("/v1/orders", json={"menu_id": 1, "qty": 5})
    assert r_201.status_code == 201
    order = r_201.json()
    assert order["status"] == "baru"
    expected_total = 60000 * (100 - aturan.DISKON_PERSEN) // 100 if 60000 >= aturan.BATAS_DISKON else 60000
    assert order["total"] == expected_total

    menu_after = client.get("/v1/menus/1").json()
    assert menu_after["stock"] == 15


# ---------- GET /v1/orders/{order_id} & POST /v1/orders/{order_id}/batal ----------


def test_get_and_cancel_order(client: TestClient):
    missing = client.get("/v1/orders/99999")
    require_implemented(missing, feature="GET /v1/orders/{order_id}")
    assert missing.status_code == 404

    created = client.post("/v1/orders", json={"menu_id": 2, "qty": 2})
    require_implemented(created, feature="POST /v1/orders")
    assert created.status_code == 201
    order_id = created.json()["id"]

    fetched = client.get(f"/v1/orders/{order_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == order_id

    cancel_1 = client.post(f"/v1/orders/{order_id}/batal")
    require_implemented(cancel_1, feature="POST /v1/orders/{order_id}/batal")
    assert cancel_1.status_code == 200
    assert cancel_1.json()["status"] == "batal"
    assert client.get("/v1/menus/2").json()["stock"] == 15

    cancel_2 = client.post(f"/v1/orders/{order_id}/batal")
    assert cancel_2.status_code == 409
    assert cancel_2.json().get("detail") == "Pesanan sudah dibatalkan"


# ---------- Bonus routes ----------


def test_bonus_orders_list_and_laporan(client: TestClient):
    laporan_empty = client.get("/v1/laporan")
    require_implemented(laporan_empty, feature="GET /v1/laporan")
    assert laporan_empty.status_code == 200
    assert laporan_empty.json() == {"jumlah_pesanan": 0, "pendapatan": 0}

    orders_list = client.get("/v1/orders")
    require_implemented(orders_list, feature="GET /v1/orders")
    assert orders_list.status_code == 200
    assert orders_list.json() == []
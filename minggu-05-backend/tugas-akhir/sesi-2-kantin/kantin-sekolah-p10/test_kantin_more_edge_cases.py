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


# ---------- Additional menu edge cases ----------


def test_post_menu_default_stock_and_price_multiple(client: TestClient):
    r_default = client.post(
        "/v1/menus",
        json={"name": "Es Teh Manis", "category": "minuman", "price": 11000},
    )
    require_implemented(r_default, feature="POST /v1/menus")
    assert r_default.status_code == 201
    assert r_default.json()["stock"] == 0
    assert r_default.json()["price"] == 11000

    r_bad_step = client.post(
        "/v1/menus",
        json={"name": "Es Jeruk Peras", "category": "minuman", "price": 11250, "stock": 5},
    )
    assert r_bad_step.status_code == 422


def test_patch_menu_category_and_stock_updates(client: TestClient):
    r_patch = client.patch(
        "/v1/menus/4",  # Es Teh: minuman, 3000, stock=50
        json={"category": "makanan", "stock": 25},
    )
    require_implemented(r_patch, feature="PATCH /v1/menus/{menu_id}")
    assert r_patch.status_code == 200
    body = r_patch.json()
    assert body["category"] == "makanan"
    assert body["stock"] == 25
    assert body["price"] == 3000


# ---------- Additional order & cancel edge cases ----------


def test_order_400_and_409_within_qty_range_leave_stock_unchanged(client: TestClient):
    # 400 when menu_id does not exist
    r_400 = client.post("/v1/orders", json={"menu_id": 99999, "qty": 1})
    require_implemented(r_400, feature="POST /v1/orders")
    assert r_400.status_code == 400
    assert r_400.json().get("detail") == "Menu tidak ditemukan"

    # 409 when qty is valid (e.g. QTY_MAX) but stock is 0 (Roti Bakar id=3)
    r_409 = client.post("/v1/orders", json={"menu_id": 3, "qty": aturan.QTY_MAX})
    assert r_409.status_code == 409
    assert r_409.json().get("detail") == "Stok tidak cukup"
    assert client.get("/v1/menus/3").json()["stock"] == 0


def test_order_below_discount_threshold_keeps_full_subtotal(client: TestClient):
    # Mi Ayam id=2: price=10000, qty=4 -> subtotal=40000 (< 50000), no discount
    resp = client.post("/v1/orders", json={"menu_id": 2, "qty": 4})
    require_implemented(resp, feature="POST /v1/orders")
    assert resp.status_code == 201
    assert resp.json()["total"] == 40000


def test_cancel_missing_404_and_double_cancel_does_not_double_restore_stock(client: TestClient):
    r_404 = client.post("/v1/orders/99999/batal")
    require_implemented(r_404, feature="POST /v1/orders/{order_id}/batal")
    assert r_404.status_code == 404

    created = client.post("/v1/orders", json={"menu_id": 6, "qty": 3})  # Air Mineral stock 30 -> 27
    require_implemented(created, feature="POST /v1/orders")
    assert created.status_code == 201
    order_id = created.json()["id"]
    assert client.get("/v1/menus/6").json()["stock"] == 27

    first_cancel = client.post(f"/v1/orders/{order_id}/batal")
    assert first_cancel.status_code == 200
    assert client.get("/v1/menus/6").json()["stock"] == 30

    second_cancel = client.post(f"/v1/orders/{order_id}/batal")
    assert second_cancel.status_code == 409
    assert second_cancel.json().get("detail") == "Pesanan sudah dibatalkan"
    assert client.get("/v1/menus/6").json()["stock"] == 30


def test_laporan_zero_when_all_orders_cancelled(client: TestClient):
    created = client.post("/v1/orders", json={"menu_id": 4, "qty": 2})
    require_implemented(created, feature="POST /v1/orders")
    assert created.status_code == 201
    order_id = created.json()["id"]

    cancel_r = client.post(f"/v1/orders/{order_id}/batal")
    require_implemented(cancel_r, feature="POST /v1/orders/{order_id}/batal")
    assert cancel_r.status_code == 200

    laporan_r = client.get("/v1/laporan")
    require_implemented(laporan_r, feature="GET /v1/laporan")
    assert laporan_r.status_code == 200
    assert laporan_r.json() == {"jumlah_pesanan": 0, "pendapatan": 0}
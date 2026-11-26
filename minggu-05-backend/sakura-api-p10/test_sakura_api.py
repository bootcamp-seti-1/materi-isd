import os
import subprocess
from datetime import date, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_SQL = BASE_DIR / "db" / "schema.sql"
SEED_SQL = BASE_DIR / "db" / "seed.sql"


def _load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            values[key.strip()] = val.strip().strip('"').strip("'")
    for key, val in os.environ.items():
        values[key] = val
    return values


def reset_sakura_db() -> None:
    cfg = _load_env()
    host = cfg.get("DB_HOST", "127.0.0.1")
    port = cfg.get("DB_PORT", "3306")
    user = cfg.get("DB_USER")
    password = cfg.get("DB_PASSWORD", "")
    db_name = cfg.get("DB_NAME", "sakura_db")

    assert user and db_name, "DB_USER and DB_NAME must be set in .env or environment."

    cmd = ["mysql", f"-h{host}", f"-P{port}", f"-u{user}"]
    env = os.environ.copy()
    if password:
        env["MYSQL_PWD"] = password

    for sql_path in (SCHEMA_SQL, SEED_SQL):
        assert sql_path.exists(), f"Missing SQL file: {sql_path}"
        with sql_path.open("rb") as fh:
            proc = subprocess.run(
                [*cmd, db_name],
                stdin=fh,
                capture_output=True,
                text=True,
                env=env,
            )
        if proc.returncode != 0:
            pytest.fail(f"Failed applying {sql_path.name}: {proc.stderr.strip()}")


@pytest.fixture(autouse=True)
def fresh_db():
    reset_sakura_db()
    yield


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


# ---------- Health & GET /v1/tasks ----------


def test_beranda(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "dokumentasi" in resp.json()


def test_list_tasks_filter_pagination_and_detail(client: TestClient):
    all_resp = client.get("/v1/tasks")
    assert all_resp.status_code == 200
    tasks = all_resp.json()
    assert len(tasks) == 8
    assert "created_at" in tasks[0]

    todo_resp = client.get("/v1/tasks", params={"status": "todo"})
    assert todo_resp.status_code == 200
    assert [t["id"] for t in todo_resp.json()] == [3, 5, 6, 8]

    paged_resp = client.get("/v1/tasks", params={"priority": 1, "limit": 2, "offset": 0})
    assert paged_resp.status_code == 200
    assert [t["id"] for t in paged_resp.json()] == [1, 2]

    bad_status = client.get("/v1/tasks", params={"status": "selesai"})
    assert bad_status.status_code == 422

    bad_limit = client.get("/v1/tasks", params={"limit": 500})
    assert bad_limit.status_code == 422
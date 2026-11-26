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

    detail_resp = client.get("/v1/tasks/2")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == 2

    missing = client.get("/v1/tasks/999")
    assert missing.status_code == 404
    assert missing.json().get("detail") == "Task 999 tidak ditemukan"

    invalid_id = client.get("/v1/tasks/abc")
    assert invalid_id.status_code == 422


# ---------- POST /v1/tasks & Validation ----------


def test_create_task_and_validation_errors(client: TestClient):
    future_date = (date.today() + timedelta(days=7)).isoformat()
    created = client.post(
        "/v1/tasks",
        json={
            "project_id": 2,
            "title": "   Export rekap ke Excel   ",
            "priority": 1,
            "due_date": future_date,
        },
    )
    assert created.status_code == 201
    data = created.json()
    assert data["id"] == 9
    assert data["title"] == "Export rekap ke Excel"
    assert data["status"] == "todo"
    assert data["due_date"] == future_date

    blank_title = client.post(
        "/v1/tasks",
        json={"project_id": 1, "title": "   "},
    )
    assert blank_title.status_code == 422

    bad_priority = client.post(
        "/v1/tasks",
        json={"project_id": 1, "title": "Tugas Uji", "priority": 99},
    )
    assert bad_priority.status_code == 422

    past_date = client.post(
        "/v1/tasks",
        json={"project_id": 1, "title": "Tugas Uji", "due_date": "2020-01-01"},
    )
    assert past_date.status_code == 422
    assert "due_date tidak boleh tanggal yang sudah lewat" in str(past_date.json())

    extra_field = client.post(
        "/v1/tasks",
        json={"project_id": 1, "title": "Tugas Uji", "assignee": "Budi"},
    )
    assert extra_field.status_code == 422

    missing_project = client.post(
        "/v1/tasks",
        json={"project_id": 99, "title": "Tugas Uji"},
    )
    assert missing_project.status_code == 400
    assert missing_project.json().get("detail") == "Project 99 tidak ada"


# ---------- PATCH, PUT, DELETE /v1/tasks/{task_id} ----------


def test_patch_put_and_delete_task(client: TestClient):
    patched = client.patch("/v1/tasks/3", json={"status": "doing", "priority": 1})
    assert patched.status_code == 200
    assert patched.json()["status"] == "doing"
    assert patched.json()["priority"] == 1

    null_title = client.patch("/v1/tasks/3", json={"title": None})
    assert null_title.status_code == 422
    assert null_title.json().get("detail") == "Field title tidak boleh null"

    replaced = client.put(
        "/v1/tasks/3",
        json={"project_id": 1, "title": "Fitur keranjang belanja v2"},
    )
    assert replaced.status_code == 200
    assert replaced.json()["title"] == "Fitur keranjang belanja v2"
    assert replaced.json()["status"] == "todo"
    assert replaced.json()["priority"] == 2
    assert replaced.json()["due_date"] is None

    deleted_first = client.delete("/v1/tasks/8")
    assert deleted_first.status_code == 204

    deleted_second = client.delete("/v1/tasks/8")
    assert deleted_second.status_code == 404


# ---------- GET /v1/projects ----------


def test_projects_and_project_tasks(client: TestClient):
    projects_resp = client.get("/v1/projects")
    assert projects_resp.status_code == 200
    assert len(projects_resp.json()) == 3

    proj_1 = client.get("/v1/projects/1")
    assert proj_1.status_code == 200
    assert proj_1.json()["id"] == 1

    proj_missing = client.get("/v1/projects/99")
    assert proj_missing.status_code == 404

    proj_1_tasks = client.get("/v1/projects/1/tasks")
    assert proj_1_tasks.status_code == 200
    assert all(t["project_id"] == 1 for t in proj_1_tasks.json())

    proj_99_tasks = client.get("/v1/projects/99/tasks")
    assert proj_99_tasks.status_code == 404

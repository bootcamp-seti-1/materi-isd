import pytest
from db import execute, fetch_all, get_connection


@pytest.fixture(autouse=True)
def reset_database():
  """Resets database by dropping tables in correct foreign key order,

  then runs schema, seed, and g3bonus files cleanly.
  """
  conn = get_connection()
  cursor = conn.cursor()
  try:
    # Disable foreign key checks to allow dropping tables in any order
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS tasks;")
    cursor.execute("DROP TABLE IF EXISTS projects;")
    cursor.execute("DROP TABLE IF EXISTS members;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Run your actual SQL files in order
    sql_files = ["db/schema.sql", "db/seed.sql", "db/g3bonus.sql"]

    for file_path in sql_files:
      with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
        for statement in sql_content.split(";"):
          statement = statement.strip()
          if statement:
            cursor.execute(statement)

    conn.commit()
  finally:
    cursor.close()
    conn.close()


def test_fetch_projects():
  """Test Menu 1: Fetching projects."""
  projects = fetch_all("SELECT id, name, client FROM projects ORDER BY id")
  assert len(projects) > 0


def test_fetch_tasks_with_joins():
  """Test Menu 2: Fetching tasks with JOINs (including members)."""
  sql = """
        SELECT t.id, t.title, t.status, t.priority, p.name AS project_name, COALESCE(m.name, '-') AS member_name
        FROM tasks t
        JOIN projects p ON p.id = t.project_id
        LEFT JOIN members m ON m.id = t.member_id
        ORDER BY t.priority, t.id
    """
  tasks = fetch_all(sql)
  assert isinstance(tasks, list)


def test_add_task_and_security():
  """Test Menu 3 & G1 Security: Adding a task safely with special characters."""
  malicious_title = "Rapat dengan klien 'Kopi' x'); DROP TABLE tasks; --"

  execute(
      "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
      (1, malicious_title, 1),
  )

  tasks = fetch_all("SELECT title FROM tasks WHERE project_id = 1")
  titles = [t["title"] for t in tasks]
  assert malicious_title in titles


def test_update_status():
  """Test Menu 4: Updating task status."""
  execute("UPDATE tasks SET status = %s WHERE id = %s", ("done", 1))
  task = fetch_all("SELECT status FROM tasks WHERE id = 1")
  assert task[0]["status"] == "done"


def test_delete_task():
  """Test Menu 5: Deleting a task."""
  tasks = fetch_all("SELECT id FROM tasks LIMIT 1")
  if tasks:
    task_id = tasks[0]["id"]
    execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    remaining = fetch_all("SELECT id FROM tasks WHERE id = %s", (task_id,))
    assert len(remaining) == 0


def test_laporan_aggregations():
  """Test Menu 6: Report with LEFT JOIN and COALESCE."""
  sql = """
        SELECT p.name, 
               COUNT(t.id) AS jumlah, 
               COALESCE(SUM(t.status = 'done'), 0) AS selesai
        FROM projects p
        LEFT JOIN tasks t ON t.project_id = p.id
        GROUP BY p.id, p.name
        ORDER BY p.id
    """
  report = fetch_all(sql)
  assert len(report) > 0


def test_search_tasks():
  """Test Menu 7 (Bonus): Searching tasks with LIKE pattern."""
  sql = "SELECT t.id, t.title FROM tasks t WHERE t.title LIKE %s"
  results = fetch_all(sql, ("%%",))
  assert isinstance(results, list)
import pytest
from db import execute, fetch_all, get_connection


@pytest.fixture(autouse=True)
def reset_database():
  """Resets and seeds the database cleanly before running security tests."""
  conn = get_connection()
  cursor = conn.cursor()
  try:
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS tasks;")
    cursor.execute("DROP TABLE IF EXISTS projects;")
    cursor.execute("DROP TABLE IF EXISTS members;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    sql_files = ["db/schema.sql", "db/seed.sql", "db/g3bonus.sql"]
    for file_path in sql_files:
      with open(file_path, "r", encoding="utf-8") as f:
        for statement in f.read().split(";"):
          statement = statement.strip()
          if statement:
            cursor.execute(statement)

    conn.commit()
  finally:
    cursor.close()
    conn.close()


def test_sql_injection_drop_table_attack():
  """Simulate Rani's attack: Injecting a DROP TABLE payload into task titles.

  Verifies that parameterization (%s) safely treats the payload as a literal string
  rather than executing SQL commands, leaving the database intact.
  """
  malicious_title = "x'); DROP TABLE tasks; --"

  # Attempt the injection attack via the secure execute function
  execute(
      "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
      (1, malicious_title, 1),
  )

  # 1. Verify the tasks table still exists and didn't get dropped
  tables = fetch_all("SHOW TABLES LIKE 'tasks'")
  assert len(tables) == 1, "CRITICAL: The tasks table was dropped by SQL injection!"

  # 2. Verify the malicious payload was safely stored as a literal string title
  tasks = fetch_all("SELECT title FROM tasks WHERE title = %s", (malicious_title,))
  assert len(tasks) == 1
  assert tasks[0]["title"] == malicious_title


def test_sql_injection_quotes_attack():
  """Verify that single quotes within inputs (e.g.

  Rapat dengan klien 'Kopi')
  do not cause syntax errors or break query execution.
  """
  tricky_title = "Rapat dengan klien 'Kopi'"

  execute(
      "INSERT INTO tasks (project_id, title, priority) VALUES (%s, %s, %s)",
      (1, tricky_title, 2),
  )

  # Verify it is fetched correctly without throwing a syntax error
  tasks = fetch_all(
      "SELECT title FROM tasks WHERE title = %s", (tricky_title,)
  )
  assert len(tasks) == 1
  assert tasks[0]["title"] == tricky_title
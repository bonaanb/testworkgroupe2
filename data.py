import sqlite3

TASKS_DB = "tasks.db"
COMPLETED_DB = "completed.db"


# ---------- INIT ----------
def init_db():
    # tasks.db
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

    # completed.db
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


# ---------- TASKS ----------
def show_tasks() -> list:
    """Получить все активные задачи"""
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def insert_task(name: str) -> None:
    """Добавить задачу"""
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()


def get_task_by_id(task_id: int):
    """Получить задачу по id"""
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM tasks WHERE id = ?",
        (task_id,)
    )
    task = cursor.fetchone()
    conn.close()
    return task


def delete_task(task_id: int) -> None:
    """Удалить задачу"""
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()


# ---------- COMPLETED ----------
def add_completed(name: str) -> None:
    """Добавить выполненную задачу"""
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO completed (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    conn.close()


def show_completed() -> list:
    """Получить все выполненные задачи"""
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM completed")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete()


if __name__ == "__main__":
    print("TASKS:", show_tasks())
    print("COMPLETED:", show_completed())

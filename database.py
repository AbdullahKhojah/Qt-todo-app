import sqlite3

import bcrypt


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(r"C:\Users\bobok\PycharmProjects\PythonProject5\AuthDB.db")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                time TEXT,
                effort TEXT,
                done INTEGER DEFAULT 0,
                type TEXT CHECK(type IN ('quick', 'detailed')),
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Auth(id)
            )
        """)
        self.conn.commit()

    def add_task(self, title, task_type, user_id, time=None, effort=None):
        self.cursor.execute("""
            INSERT INTO tasks (title, type, user_id, time, effort)
            VALUES (?, ?, ?, ?, ?)
        """, (title, task_type, user_id, time, effort))
        self.conn.commit()

    def get_tasks(self, user_id, task_type=None):
        if task_type:
            self.cursor.execute("SELECT * FROM tasks WHERE user_id = ? AND type = ?", (user_id, task_type))
        else:
            self.cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def mark_task_done(self, task_id):
        self.cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

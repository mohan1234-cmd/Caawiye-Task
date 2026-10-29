from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        task TEXT,
        deadline TEXT,
        completed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    c.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
    pending_tasks = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed_tasks = c.fetchone()[0]

    progress = 0
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total_tasks,
        pending=pending_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )


@app.route("/add", methods=["POST"])
def add():
    subject = request.form["subject"]
    task = request.form["task"]
    deadline = request.form["deadline"]

    if subject and task:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO tasks(subject, task, deadline) VALUES (?, ?, ?)",
            (subject, task, deadline)
        )
        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

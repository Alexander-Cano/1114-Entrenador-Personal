from datetime import date, timedelta
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, send_from_directory

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "ritmo.db"
app = Flask(__name__)


def db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with db() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY, title TEXT NOT NULL, duration INTEGER NOT NULL,
                level TEXT NOT NULL, icon TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS workout_log (
                id INTEGER PRIMARY KEY, workout_id INTEGER NOT NULL, completed_on TEXT NOT NULL,
                minutes INTEGER NOT NULL DEFAULT 0, progress INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(workout_id) REFERENCES workouts(id)
            );
        """)
        if not connection.execute("SELECT 1 FROM users").fetchone():
            connection.execute("INSERT INTO users (name) VALUES (?)", ("Valeria",))
            connection.executemany(
                "INSERT INTO workouts (title, duration, level, icon) VALUES (?, ?, ?, ?)",
                [("Fuerza de cuerpo completo", 35, "Nivel intermedio", "🏋️"),
                 ("Movilidad para corredores", 12, "Nivel suave", "🧘")],
            )
            today = date.today()
            connection.executemany(
                "INSERT INTO workout_log (workout_id, completed_on, minutes, progress) VALUES (?, ?, ?, ?)",
                [(1, (today - timedelta(days=1)).isoformat(), 35, 35),
                 (1, (today - timedelta(days=2)).isoformat(), 35, 35),
                 (1, (today - timedelta(days=3)).isoformat(), 35, 35),
                 (2, today.isoformat(), 0, 8)],
            )


@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/dashboard")
def dashboard():
    today = date.today()
    with db() as connection:
        user = connection.execute("SELECT name FROM users LIMIT 1").fetchone()
        current = connection.execute("SELECT * FROM workouts WHERE id = 1").fetchone()
        continuing = connection.execute("""
            SELECT w.*, l.progress FROM workout_log l JOIN workouts w ON w.id = l.workout_id
            WHERE l.progress > 0 AND l.progress < w.duration ORDER BY l.completed_on DESC LIMIT 1
        """).fetchone()
        week_start = today - timedelta(days=today.weekday())
        week_minutes = connection.execute("SELECT COALESCE(SUM(minutes), 0) total FROM workout_log WHERE completed_on >= ?", (week_start.isoformat(),)).fetchone()["total"]
        streak = connection.execute("SELECT COUNT(DISTINCT completed_on) count FROM workout_log WHERE minutes > 0").fetchone()["count"]
    week = []
    for offset in range(6):
        day = week_start + timedelta(days=offset)
        week.append({"date": day.isoformat(), "name": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"][offset], "number": day.day, "active": day == today})
    return jsonify({
        "user": dict(user), "today_label": today.strftime("%A, %d de %B").capitalize(),
        "today_workout": dict(current), "continue_workout": dict(continuing),
        "stats": {"streak": streak, "week_minutes": week_minutes}, "week": week,
    })


@app.post("/api/workouts/today/start")
def start_workout():
    with db() as connection:
        connection.execute("INSERT INTO workout_log (workout_id, completed_on, minutes, progress) VALUES (1, ?, 35, 35)", (date.today().isoformat(),))
    return jsonify({"message": "¡Entrenamiento guardado! Sumaste 35 minutos."})


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=5000)

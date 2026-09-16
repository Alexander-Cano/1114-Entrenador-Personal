from datetime import date, timedelta
from pathlib import Path
import sqlite3
from flask import Flask, Response, redirect, send_from_directory, url_for, request, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, Response, redirect, send_from_directory, url_for

# Carpetas del proyecto
ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
ESTILOS = ROOT / "estilos"
IMG = ROOT / "IMG"

# Base de datos
DATABASE = ROOT / "ritmo.db"

app = Flask(__name__)

app.secret_key = "kenesis-clave-secreta"


def db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with db() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                duration INTEGER NOT NULL,
                level TEXT NOT NULL,
                icon TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS workout_log (
                id INTEGER PRIMARY KEY,
                workout_id INTEGER NOT NULL,
                completed_on TEXT NOT NULL,
                minutes INTEGER NOT NULL DEFAULT 0,
                progress INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(workout_id) REFERENCES workouts(id)
            );
                CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
        """)

        user_exists = connection.execute(
            "SELECT 1 FROM users"
        ).fetchone()

        if not user_exists:
            connection.execute(
                "INSERT INTO users (name) VALUES (?)",
                ("Valeria",)
            )

            connection.executemany(
                """
                INSERT INTO workouts
                (title, duration, level, icon)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        "Fuerza de cuerpo completo",
                        35,
                        "Nivel intermedio",
                        "🏋️"
                    ),
                    (
                        "Movilidad para corredores",
                        12,
                        "Nivel suave",
                        "🧘"
                    )
                ]
            )


@app.get("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    with db() as connection:
        minutes = connection.execute(
            """
            SELECT COALESCE(SUM(minutes), 0) AS total
            FROM workout_log
            WHERE completed_on >= ?
            """,
            (week_start.isoformat(),)
        ).fetchone()["total"]

        streak = connection.execute(
            """
            SELECT COUNT(DISTINCT completed_on) AS total
            FROM workout_log
            WHERE minutes > 0
            """
        ).fetchone()["total"]

    html = (TEMPLATES / "index.html").read_text(encoding="utf-8")

    html = html.replace("[[NAME]]", session["user_name"])
    html = html.replace(
        "[[TODAY]]",
        today.strftime("%A, %d de %B").capitalize()
    )
    html = html.replace("[[STREAK]]", str(streak))
    html = html.replace("[[MINUTES]]", str(minutes))

    return Response(html, mimetype="text/html")


@app.get("/estilos/index.css")
def styles():
    return send_from_directory(ESTILOS, "index.css")


@app.get("/IMG/LOGO.png")
def logo():
    return send_from_directory(IMG, "LOGO.png")


@app.post("/start")
def start_workout():
    with db() as connection:
        connection.execute(
            """
            INSERT INTO workout_log
            (workout_id, completed_on, minutes, progress)
            VALUES (?, ?, ?, ?)
            """,
            (
                1,
                date.today().isoformat(),
                35,
                35
            )
        )

    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with db() as connection:
            account = connection.execute(
                "SELECT * FROM accounts WHERE email = ?",
                (email,)
            ).fetchone()

        if account and check_password_hash(account["password"], password):
            session["user_id"] = account["id"]
            session["user_name"] = account["name"]
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Correo o contraseña incorrectos."
        )

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            with db() as connection:
                connection.execute(
                    """
                    INSERT INTO accounts (name, email, password)
                    VALUES (?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        generate_password_hash(password)
                    )
                )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Este correo ya está registrado."
            )

    return render_template("register.html")


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=5000)
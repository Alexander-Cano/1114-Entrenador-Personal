from datetime import date, timedelta
from functools import wraps
import os
from pathlib import Path
import sqlite3

from flask import (
    Flask, abort, flash, redirect, render_template, request,
    send_from_directory, session, url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "ritmo.db"
ESTILOS = ROOT / "estilos"
IMG = ROOT / "IMG"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "KENSIS_SECRET_KEY",
    "kenesis-clave-secreta-cambia-en-produccion",
)

DAYS = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
MONTHS = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)


def db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
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
            """
        )
        if not connection.execute("SELECT 1 FROM workouts LIMIT 1").fetchone():
            connection.executemany(
                """
                INSERT INTO workouts (title, duration, level, icon)
                VALUES (?, ?, ?, ?)
                """,
                [
                    ("Fuerza de cuerpo completo", 35, "Nivel intermedio", "🏋️"),
                    ("Movilidad para corredores", 12, "Nivel suave", "🧘"),
                    ("Cardio de resistencia", 30, "Nivel avanzado", "⚡"),
                ],
            )


initialize_database()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.full_path))
        return view(*args, **kwargs)
    return wrapped_view


def format_date(value):
    return f"{DAYS[value.weekday()]}, {value.day} de {MONTHS[value.month - 1]}"


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return date.today()


def get_initials(name):
    parts = [part for part in name.strip().split() if part]
    return "".join(part[0] for part in parts[:2]).upper() or "K"


def get_streak(log_dates, today):
    if not log_dates:
        return 0
    cursor = today if today in log_dates else today - timedelta(days=1)
    streak = 0
    while cursor in log_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def dashboard_data(selected_raw=None):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    selected_day = parse_date(selected_raw)
    if not week_start <= selected_day <= week_start + timedelta(days=6):
        selected_day = today

    with db() as connection:
        workouts = connection.execute(
            "SELECT * FROM workouts ORDER BY id"
        ).fetchall()
        logs = connection.execute(
            """
            SELECT completed_on, minutes
            FROM workout_log
            WHERE minutes > 0
            ORDER BY completed_on DESC, id DESC
            """
        ).fetchall()
        recent_logs = connection.execute(
            """
            SELECT workout_log.completed_on, workout_log.minutes,
                   workouts.title, workouts.icon
            FROM workout_log
            JOIN workouts ON workouts.id = workout_log.workout_id
            WHERE workout_log.minutes > 0
            ORDER BY workout_log.completed_on DESC, workout_log.id DESC
            LIMIT 8
            """
        ).fetchall()

    minutes_by_day = {}
    logged_dates = set()
    for log in logs:
        logged_on = parse_date(log["completed_on"])
        logged_dates.add(logged_on)
        minutes_by_day[logged_on] = minutes_by_day.get(logged_on, 0) + log["minutes"]

    week_days = []
    for offset in range(7):
        current = week_start + timedelta(days=offset)
        week_days.append(
            {
                "iso": current.isoformat(),
                "label": DAYS[current.weekday()],
                "number": current.day,
                "is_today": current == today,
                "is_selected": current == selected_day,
                "completed": current in logged_dates,
                "minutes": minutes_by_day.get(current, 0),
            }
        )

    weekly_minutes = sum(
        minutes for logged_on, minutes in minutes_by_day.items()
        if week_start <= logged_on <= week_start + timedelta(days=6)
    )
    total_minutes = sum(minutes_by_day.values())
    total_sessions = len(logs)
    user_name = session.get("user_name", "Atleta")
    return {
        "user_name": user_name,
        "user_email": session.get("user_email", ""),
        "user_initials": get_initials(user_name),
        "today_label": format_date(today),
        "selected_day_label": format_date(selected_day),
        "selected_day_minutes": minutes_by_day.get(selected_day, 0),
        "selected_day_completed": selected_day in logged_dates,
        "week_days": week_days,
        "workouts": workouts,
        "current_workout": workouts[0] if workouts else None,
        "weekly_minutes": weekly_minutes,
        "total_minutes": total_minutes,
        "total_sessions": total_sessions,
        "streak": get_streak(logged_dates, today),
        "activity_score": min(100, round(weekly_minutes / 150 * 100)),
        "recent_logs": recent_logs,
    }


@app.get("/")
@login_required
def home():
    return render_template("index.html", **dashboard_data(request.args.get("day")))


@app.get("/estilos/<path:filename>")
def styles(filename):
    return send_from_directory(ESTILOS, filename)


@app.get("/IMG/<path:filename>")
def logo(filename):
    return send_from_directory(IMG, filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        with db() as connection:
            account = connection.execute(
                """
                SELECT id, name, email, password FROM accounts
                WHERE lower(email) = lower(?) LIMIT 1
                """,
                (email,),
            ).fetchone()
        if account and check_password_hash(account["password"], password):
            session.clear()
            session["user_id"] = account["id"]
            session["user_name"] = account["name"].strip()
            session["user_email"] = account["email"]
            return redirect(request.args.get("next") or url_for("home"))
        return render_template(
            "login.html", error="Correo o contraseña incorrectos.", email=email
        )
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(name) < 2:
            return render_template("register.html", error="Escribe tu nombre para continuar.")
        if len(password) < 6:
            return render_template(
                "register.html",
                error="La contraseña debe tener al menos 6 caracteres.",
            )
        try:
            with db() as connection:
                connection.execute(
                    "INSERT INTO accounts (name, email, password) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
        except sqlite3.IntegrityError:
            return render_template(
                "register.html", error="Este correo ya está registrado."
            )
        flash("Cuenta creada. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/home")
@login_required
def nav_home():
    return redirect(url_for("home"))


@app.route("/start", methods=["GET", "POST"])
@login_required
def start():
    return redirect(url_for("comenzar"))


@app.get("/comenzar")
@login_required
def comenzar():
    workout_id = request.args.get("workout", type=int)
    with db() as connection:
        workout = connection.execute(
            "SELECT * FROM workouts WHERE id = ?",
            (workout_id,),
        ).fetchone() if workout_id else connection.execute(
            "SELECT * FROM workouts ORDER BY id LIMIT 1"
        ).fetchone()
    if workout is None:
        abort(404)
    return render_template("Comenzar.html", workout=workout, **dashboard_data())


@app.post("/workouts/<int:workout_id>/complete")
@login_required
def complete_workout(workout_id):
    with db() as connection:
        workout = connection.execute(
            "SELECT * FROM workouts WHERE id = ?", (workout_id,)
        ).fetchone()
        if workout is None:
            abort(404)
        connection.execute(
            """
            INSERT INTO workout_log
                (workout_id, completed_on, minutes, progress)
            VALUES (?, ?, ?, ?)
            """,
            (workout_id, date.today().isoformat(), workout["duration"], 100),
        )
    flash(f"¡Buen trabajo! Completaste «{workout['title']}».", "success")
    return redirect(url_for("home"))


@app.get("/calendar")
@login_required
def calendar():
    return render_template(
        "plan.html", calendar_view=True, **dashboard_data(request.args.get("day"))
    )


@app.get("/day/<day>")
@login_required
def select_day(day):
    selected = parse_date(day)
    if selected.isoformat() != day:
        flash("Ese día no está disponible en el calendario.", "error")
        return redirect(url_for("home"))
    return redirect(url_for("home", day=selected.isoformat()))


@app.get("/plan")
@login_required
def nav_plan():
    return render_template("plan.html", calendar_view=False, **dashboard_data())


@app.get("/progress/streak")
@login_required
def progress_streak():
    return redirect(url_for("nav_progress") + "#streak")


@app.get("/progress/minutes")
@login_required
def progress_minutes():
    return redirect(url_for("nav_progress") + "#minutes")


@app.get("/progress")
@login_required
def nav_progress():
    return render_template("progress.html", **dashboard_data())


@app.get("/profile")
@login_required
def nav_profile():
    return render_template("profile.html", **dashboard_data())


@app.errorhandler(404)
def not_found(_error):
    return render_template("login.html", error="La página que buscas no existe."), 404


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )

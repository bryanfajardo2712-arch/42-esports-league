import re
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "league.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "desarrollo-local-cambia-esto"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL
            )
            """
        )


def intra_photo_url(username):
    return f"https://cdn.intra.42.fr/users/{username}.jpg"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        display_name = request.form.get("display_name", "").strip()

        if not re.fullmatch(r"[a-z0-9_-]{2,20}", username):
            flash("El usuario debe tener entre 2 y 20 caracteres: letras, numeros, '-' o '_'.")
        elif not display_name:
            flash("El nombre visible es obligatorio.")
        else:
            try:
                with get_db() as connection:
                    connection.execute(
                        "INSERT INTO players (username, display_name) VALUES (?, ?)",
                        (username, display_name),
                    )
                flash(f"{display_name} fue agregado correctamente.")
            except sqlite3.IntegrityError:
                flash("Ese usuario de 42 ya esta registrado.")

        return redirect(url_for("index"))

    with get_db() as connection:
        players = connection.execute(
            "SELECT id, username, display_name FROM players ORDER BY display_name COLLATE NOCASE"
        ).fetchall()

    return render_template(
        "index.html",
        players=players,
        intra_photo_url=intra_photo_url,
    )


@app.post("/players/<int:player_id>/delete")
def delete_player(player_id):
    with get_db() as connection:
        connection.execute("DELETE FROM players WHERE id = ?", (player_id,))
    flash("Jugador eliminado.")
    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)

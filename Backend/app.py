import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR.parent / "Templates"),
    static_folder=str(BASE_DIR.parent / "Templates" / "static"),
    static_url_path="/static",
)
app.secret_key = "student-comfort-secret-key"


def get_db_connection():
    conn = sqlite3.connect(BASE_DIR / "Student_Comfort.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS houses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT NOT NULL,
                image_url TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO houses (name, address, price, description, image_url)
            VALUES
                ('Self Content', 'Pankshin, Plateau State', 100000, 'Comfortable student room with reliable security and electricity.', 'images/Image 1'),
                ('Premier Lodge', 'Jos, Plateau State', 120000, 'Secure accommodation close to campus and transport routes.', 'images/IMage 2'),
                ('Campus View', 'Pankshin, Plateau State', 95000, 'Affordable and well-kept rooms for students.', 'images/image 3'),
                ('Green Valley', 'Jos, Plateau State', 110000, 'Spacious rooms with water supply and a peaceful environment.', 'images/image 4')
            """
        )


init_db()


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    with get_db_connection() as conn:
        houses = conn.execute("SELECT * FROM houses ORDER BY id").fetchall()
    return render_template("index.html", houses=houses)


@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/contact")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/houses")
@app.route("/houses.html")
def houses():
    with get_db_connection() as conn:
        houses = conn.execute("SELECT * FROM houses ORDER BY id").fetchall()
    return render_template("houses.html", houses=houses)


@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return render_template("register.html", error="Please complete all fields.")

        try:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password),
                )
        except sqlite3.IntegrityError:
            return render_template("register.html", error="That email is already registered.")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password),
            ).fetchone()

        if user is None:
            return render_template("login.html", error="Invalid email or password.")

        return redirect(url_for("index"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
import sqlite3
from pathlib import Path
import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR.parent / "Templates"),
    static_folder=str(BASE_DIR.parent / "Templates" / "static"),
    static_url_path="/static",
)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
)


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
            CREATE TABLE IF NOT EXISTS contact_messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        if conn.execute("SELECT COUNT(*) FROM houses").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO houses (name, address, price, description, image_url)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ("Self Content", "Pankshin, Plateau State", 100000, "Comfortable student room with reliable security and electricity.", "images/Image 1.jpg"),
                    ("Premier Lodge", "Jos, Plateau State", 120000, "Secure accommodation close to campus and transport routes.", "images/IMage 2.jpg"),
                    ("Campus View", "Pankshin, Plateau State", 95000, "Affordable and well-kept rooms for students.", "images/image 3.jpg"),
                    ("Green Valley", "Jos, Plateau State", 110000, "Spacious rooms with water supply and a peaceful environment.", "images/image 4.jpg"),
                ],
            )
        conn.execute(
            "UPDATE houses SET image_url = 'images/Image 1.jpg' WHERE image_url = 'images/Image 1'"
        )
        conn.execute(
            "UPDATE houses SET image_url = 'images/IMage 2.jpg' WHERE image_url = 'images/IMage 2'"
        )
        conn.execute(
            "UPDATE houses SET image_url = 'images/image 3.jpg' WHERE image_url = 'images/image 3'"
        )
        conn.execute(
            "UPDATE houses SET image_url = 'images/image 4.jpg' WHERE image_url = 'images/image 4'"
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


@app.route("/contact", methods=["GET", "POST"])
@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        description = request.form.get("description", "").strip()

        if not fullname or not email or not phone or len(description) < 20:
            return render_template(
                "contact.html",
                error="Please complete all fields. Your description must be at least 20 characters.",
            )

        with get_db_connection() as conn:
            conn.execute(
                """
                INSERT INTO contact_messages (fullname, email, phone, description)
                VALUES (?, ?, ?, ?)
                """,
                (fullname, email, phone, description),
            )
        return render_template("contact.html", success="Your message has been sent.")

    return render_template("contact.html")


@app.route("/houses")
@app.route("/houses.html")
def houses():
    query = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    page = request.args.get("page", 1, type=int)
    page = max(page, 1)
    per_page = 6

    where = []
    parameters = []
    if query:
        where.append("(name LIKE ? OR address LIKE ? OR description LIKE ?)")
        search = f"%{query}%"
        parameters.extend([search, search, search])
    if location:
        where.append("address LIKE ?")
        parameters.append(f"%{location}%")
    if min_price is not None:
        where.append("price >= ?")
        parameters.append(min_price)
    if max_price is not None:
        where.append("price <= ?")
        parameters.append(max_price)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    count_sql = f"SELECT COUNT(*) FROM houses {where_sql}"

    with get_db_connection() as conn:
        total = conn.execute(count_sql, parameters).fetchone()[0]
        total_pages = max((total + per_page - 1) // per_page, 1)
        page = min(page, total_pages)
        houses = conn.execute(
            f"""
            SELECT * FROM houses {where_sql}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            parameters + [per_page, (page - 1) * per_page],
        ).fetchall()
        locations = conn.execute(
            "SELECT DISTINCT address FROM houses ORDER BY address"
        ).fetchall()

    return render_template(
        "houses.html",
        houses=houses,
        locations=locations,
        query=query,
        location=location,
        min_price=min_price,
        max_price=max_price,
        page=page,
        total_pages=total_pages,
    )


@app.route("/houses/<int:house_id>")
def house_detail(house_id):
    with get_db_connection() as conn:
        house = conn.execute("SELECT * FROM houses WHERE id = ?", (house_id,)).fetchone()
        if house is None:
            return render_template("404.html"), 404
        related = conn.execute(
            """
            SELECT * FROM houses
            WHERE id != ? AND address LIKE ?
            ORDER BY id DESC
            LIMIT 3
            """,
            (house_id, f"%{house['address'].split(',')[-1].strip()}%"),
        ).fetchall()
    return render_template("house_detail.html", house=house, related=related)


@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return render_template("register.html", error="Please complete all fields.")
        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters.",
            )

        try:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
        except sqlite3.IntegrityError:
            return render_template("register.html", error="That email is already registered.")

        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,),
            ).fetchone()

        valid_password = False
        if user is not None:
            try:
                valid_password = check_password_hash(user["password"], password)
            except (TypeError, ValueError):
                valid_password = False

            # Upgrade legacy plaintext passwords on successful login.
            if not valid_password and user["password"] == password:
                valid_password = True
                with get_db_connection() as conn:
                    conn.execute(
                        "UPDATE users SET password = ? WHERE id = ?",
                        (generate_password_hash(password), user["id"]),
                    )

        if not valid_password:
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
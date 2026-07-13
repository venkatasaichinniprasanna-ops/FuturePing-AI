from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "futureping123"


# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect("futureping.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT,
        branch TEXT,
        career TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        type TEXT,
        link TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        branch = request.form["branch"]
        career = request.form["career"]

        conn = sqlite3.connect("futureping.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO students(fullname,email,password,branch,career)
            VALUES(?,?,?,?,?)
            """, (fullname, email, password, branch, career))

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered."

        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("futureping.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user_id"] = user[0]

            session["user"] = {
                "fullname": user[1],
                "email": user[2],
                "branch": user[4],
                "career": user[5]
            }

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        fullname=session["user"]["fullname"],
        career=session["user"]["career"]
    )


# ---------------- PROFILE ---------------- #

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("futureping.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template("profile.html", user=user)


# ---------------- OPPORTUNITIES ---------------- #

@app.route("/opportunities")
def opportunities():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    conn = sqlite3.connect("futureping.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM opportunities")
    count = cursor.fetchone()[0]

    if count == 0:

        sample_data = [
            ("Google AI Internship", "Google", "Internship", "https://careers.google.com/"),
            ("Amazon Future Engineer", "Amazon", "Scholarship", "https://www.amazonfutureengineer.com/"),
            ("Smart India Hackathon", "Government of India", "Hackathon", "https://www.sih.gov.in/"),
            ("Google Data Analytics", "Coursera", "Certification", "https://www.coursera.org/"),
            ("Microsoft Internship", "Microsoft", "Internship", "https://careers.microsoft.com/")
        ]

        cursor.executemany(
            "INSERT INTO opportunities(title,company,type,link) VALUES(?,?,?,?)",
            sample_data
        )

        conn.commit()

    if search:

        cursor.execute("""
        SELECT * FROM opportunities
        WHERE title LIKE ?
        OR company LIKE ?
        OR type LIKE ?
        """,
        ("%"+search+"%",
         "%"+search+"%",
         "%"+search+"%"))

    else:

        cursor.execute("SELECT * FROM opportunities")

    opportunities = cursor.fetchall()

    conn.close()

    return render_template(
        "opportunities.html",
        opportunities=opportunities
    )


# ---------------- ADMIN ---------------- #

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        title = request.form["title"]
        company = request.form["company"]
        type = request.form["type"]
        link = request.form["link"]

        conn = sqlite3.connect("futureping.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO opportunities(title,company,type,link)
        VALUES(?,?,?,?)
        """, (title, company, type, link))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("admin.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
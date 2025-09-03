from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import openai
import os
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# Access them like this:
api_key = os.getenv("INSTA_API_KEY")
api_url = os.getenv("INSTA_API_URL")


# ------------------ Setup ------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key in production

# ------------------ Database Connection ------------------
def get_db_connection():
    conn = sqlite3.connect("kcse_app.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ Grade-to-Point Conversion ------------------
grade_map = {
    "A": 12, "A-": 11, "B+": 10, "B": 9, "B-": 8,
    "C+": 7, "C": 6, "C-": 5, "D+": 4, "D": 3,
    "D-": 2, "E": 1
}

# ------------------ Home ------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------ Signup ------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            return "<h3>Email already registered. Try logging in.</h3><a href='/signup'>🔁 Back</a>"

    return render_template("signup.html")

# ------------------ Login ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        conn.close()

        if user:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return "<h3>Invalid credentials. Try again.</h3><a href='/login'>🔁 Back</a>"

    return render_template("login.html")

# ------------------ Logout ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ------------------ Reset Session ------------------
@app.route("/reset")
def reset():
    session.pop("cluster_score", None)
    session.pop("career_suggestions", None)
    return redirect(url_for("index"))

# ------------------ Career Advice ------------------
@app.route("/career", methods=["GET", "POST"])
def career():
    if request.method == "POST":
        interests = request.form["interests"].lower().strip()

        suggestions = []
        if "tech" in interests:
            suggestions += ["Software Engineer", "Data Scientist"]
        if "health" in interests:
            suggestions += ["Nurse", "Medical Lab Technician"]
        if "business" in interests:
            suggestions += ["Entrepreneur", "Financial Analyst"]
        if "education" in interests:
            suggestions += ["Teacher", "Education Technologist"]
        if "agriculture" in interests:
            suggestions += ["Agronomist", "Agribusiness Specialist"]
        if "engineering" in interests:
            suggestions += ["Civil Engineer", "Mechanical Engineer"]
        if not suggestions:
            suggestions.append("Try exploring fields like agriculture, education, or logistics.")

        session["career_suggestions"] = suggestions
        return redirect(url_for("dashboard"))

    return render_template("career_form.html")

# ------------------ Cluster Point Calculator ------------------
@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        grades = {
            "math": request.form["math"],
            "english": request.form["english"],
            "kiswahili": request.form["kiswahili"],
            "subject1": request.form["subject1"],
            "subject2": request.form["subject2"],
            "subject3": request.form["subject3"]
        }

        total_points = sum(grade_map.get(g.upper(), 0) for g in grades.values())
        cluster_score = round((total_points / 72) * 100, 2)

        session["cluster_score"] = cluster_score
        return redirect(url_for("dashboard"))

    return render_template("calculate.html")

# ------------------ Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    cluster_points = session.get("cluster_score", "Not calculated yet")
    career_suggestions = session.get("career_suggestions", [])
    matched_courses = ["Computer Science - UoN", "Information Technology - JKUAT"]  # Placeholder

    return render_template("dashboard.html",
                           user=session["user"],
                           cluster_points=cluster_points,
                           matched_courses=matched_courses,
                           career_suggestions=career_suggestions)

# ------------------ Show Calculate Form ------------------
@app.route("/calculate", methods=["GET"])
def show_calculate_form():
    if "user" not in session:
        return redirect("/login")
    return render_template("calculate.html")

# ------------------ AI Buddy Route ------------------
@app.route("/ai-buddy", methods=["POST"])
def ai_buddy():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    from flask import Flask, render_template, request, redirect
from intasend import initiate_payment

@app.route("/pay", methods=["GET", "POST"])
def pay():
    if request.method == "POST":
        email = request.form["email"]
        amount = request.form["amount"]
        phone = request.form["phone"]
        result = initiate_payment(email, amount, phone)
        return redirect(result["url"])  # Redirect to hosted payment page
    return render_template("pay.html")


# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(debug=True)

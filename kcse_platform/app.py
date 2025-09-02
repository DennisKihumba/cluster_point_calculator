from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key in production

# Dummy user store (for testing)
users = {
    "dennis@example.com": "password123",
    "student@kcse.com": "kcse2025"
}

# Grade-to-point conversion
grade_map = {
    "A": 12, "A-": 11, "B+": 10, "B": 9, "B-": 8,
    "C+": 7, "C": 6, "C-": 5, "D+": 4, "D": 3,
    "D-": 2, "E": 1
}

# ------------------ Home ------------------
@app.route("/")
def index():
    return render_template("index.html")

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

        return render_template("career_result.html", interests=interests, suggestions=suggestions)

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

        total_points = 0
        for grade in grades.values():
            points = grade_map.get(grade.upper(), 0)
            total_points += points

        cluster_score = round((total_points / 72) * 100, 2)  # out of 100

        return f"<h1>Your Cluster Points: {cluster_score}</h1><a href='/calculate'>🔄 Try Again</a>"

    return render_template("calculate.html")

# ------------------ Login ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email] == password:
            session["user"] = email
            return redirect(url_for("dashboard"))
        else:
            return "<h3>Invalid credentials. Try again.</h3><a href='/login'>🔁 Back</a>"

    return render_template("login.html")

# ------------------ Logout ------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# ------------------ Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    cluster_points = 72.5
    matched_courses = ["Computer Science - UoN", "Information Technology - JKUAT"]
    career_suggestions = ["Software Engineer", "Data Analyst"]

    return render_template("dashboard.html",
                           user=session["user"],
                           cluster_points=cluster_points,
                           matched_courses=matched_courses,
                           career_suggestions=career_suggestions)

# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(debug=True)

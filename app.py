from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
import hashlib
import secrets
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management

# MongoDB Configuration (Replace with your connection string)
client = MongoClient(
    "mongodb://localhost:27017"
)
db = client.quizapp
users_collection = db.users
questions_collection = db.questions
results_collection = db.results

# Utility Functions
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed_password


def check_password(salt, password, hashed_password):
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed_password


# Routes
@app.route("/")
def index():
    if "user_id" in session:
        user_role = session.get("user_role")
        if user_role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif user_role == "student":
            return redirect(url_for("student_dashboard"))
    return render_template("index.html")


# Registration Routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        # Check if user already exists (MongoDB)
        if users_collection.find_one({"username": username}):
            return render_template("register.html", error="Username already exists")

        # Hash the password
        salt, hashed_password = hash_password(password)

        # Insert user into MongoDB
        users_collection.insert_one(
            {"username": username, "password": hashed_password, "salt": salt, "role": role}
        )

        return redirect(url_for("login"))
    return render_template("register.html")


# Login Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve user from MongoDB
        user = users_collection.find_one({"username": username})

        if user and check_password(user["salt"], password, user["password"]):
            session["user_id"] = str(user["_id"])
            session["user_role"] = user["role"]
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "student":
                return redirect(url_for("student_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    return redirect(url_for("index"))


# Admin Dashboard
@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session or session.get("user_role") != "admin":
        return redirect(url_for("login"))

    # Fetch all users and questions from MongoDB
    users = list(users_collection.find())
    questions = list(questions_collection.find())

    return render_template("admin_dashboard.html", users=users, questions=questions)


@app.route("/admin/add_question", methods=["POST"])
def add_question():
    if "user_id" not in session or session.get("user_role") != "admin":
        return redirect(url_for("login"))

    question = request.form.get("question")
    options = [
        request.form.get("option1"),
        request.form.get("option2"),
        request.form.get("option3"),
        request.form.get("option4"),
    ]
    answer = request.form.get("answer")

    # Insert question into MongoDB
    questions_collection.insert_one({"question": question, "options": options, "answer": answer})

    return redirect(url_for("admin_dashboard"))


# Student Dashboard
@app.route("/student")
def student_dashboard():
    if "user_id" not in session or session.get("user_role") != "student":
        return redirect(url_for("login"))

    return render_template("student_dashboard.html")


# Quiz Routes
@app.route("/get_question", methods=["GET"])
def get_question():
    if "user_id" not in session or session.get("user_role") != "student":
        return jsonify({"error": "Unauthorized"})

    # Initialize question index in session if not present
    if "question_index" not in session:
        session["question_index"] = 0

    # Fetch questions from MongoDB
    questions = list(questions_collection.find())

    if not questions:
        return jsonify({"error": "No questions available"})

    # Get current question index
    current_index = session["question_index"]
    
    # Check if we've reached the end of questions
    if current_index >= len(questions):
        return jsonify({"error": "Quiz completed"})

    # Get the current question
    question = questions[current_index]
    
    # Increment the question index for next time
    session["question_index"] = current_index + 1

    return jsonify({
        "question": question["question"],
        "options": question["options"],
        "index": current_index,
        "total_questions": len(questions)
    })


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    if "user_id" not in session or session.get("user_role") != "student":
        return jsonify({"error": "Unauthorized"})

    data = request.get_json()
    selected_answer = data.get("answer")
    question = questions_collection.find_one({"question": data.get("question")})

    if question and selected_answer == question["answer"]:
        return jsonify({"success": True, "message": "Correct answer!"})
    else:
        return jsonify({"success": False, "message": "Incorrect answer"})


@app.route("/get_score", methods=["GET"])
def get_score():
    if "user_id" not in session or session.get("user_role") != "student":
        return jsonify({"error": "Unauthorized"})

    return jsonify({"score": 0, "username": session.get("username")})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from questions import generate_question_set

app = Flask(__name__)
CORS(app)  # allow frontend requests

# In-memory storage for users and assessments (use DB later)
users = []
assessments = []

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# Register user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    # Check if email exists
    for user in users:
        if user["email"] == data["email"]:
            return jsonify({"error": "Email already exists"}), 400

    users.append({
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]  # In production, hash this!
    })
    return jsonify({"message": "User registered successfully"}), 201

# Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    for user in users:
        if user["email"] == data.get("email") and user["password"] == data.get("password"):
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Generate practice question
@app.route("/practice", methods=["POST"])
def practice():
    data = request.get_json()
    curriculum = data.get("curriculum")
    grade = data.get("grade")
    subject = data.get("subject")

    question = generate_question_set(curriculum, grade, subject, 1)[0]
    return jsonify({"question": question})

# Generate assessment (70 questions)
@app.route("/assessment", methods=["POST"])
def assessment():
    data = request.get_json()
    curriculum = data.get("curriculum")
    grade = data.get("grade")
    subject = data.get("subject")

    questions = generate_question_set(curriculum, grade, subject, 70)
    return jsonify({"questions": questions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

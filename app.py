from flask import Flask, request, jsonify
from flask_cors import CORS
from questions import generate_questions_for_practice, generate_questions_for_assessment

app = Flask(__name__)
CORS(app)

# In-memory storage for users and assessment results
users = []
results = []

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# Register user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if email exists
    if any(u["email"] == data["email"] for u in users):
        return jsonify({"error": "Email already registered"}), 400

    users.append({
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],  # hash in production
    })
    return jsonify({"message": "User registered successfully"}), 201

# Login user
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    for u in users:
        if u["email"] == data.get("email") and u["password"] == data.get("password"):
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Practice endpoint
@app.route("/practice", methods=["POST"])
def practice():
    data = request.get_json()
    curriculum = data.get("curriculum")
    grade = data.get("grade")
    subject = data.get("subject")
    topics = data.get("topics", [])  # list of topics
    questions_per_topic = data.get("count_per_topic", 30)

    questions = generate_questions_for_practice(curriculum, grade, subject, topics, questions_per_topic)
    return jsonify({"questions": questions}), 200

# Assessment endpoint
@app.route("/assessment", methods=["POST"])
def assessment():
    data = request.get_json()
    curriculum = data.get("curriculum")
    grade = data.get("grade")
    subject = data.get("subject")
    num_questions = data.get("count", 70)

    questions = generate_questions_for_assessment(curriculum, grade, subject, num_questions)
    return jsonify({"questions": questions}), 200

# Submit assessment results
@app.route("/submit_assessment", methods=["POST"])
def submit_assessment():
    data = request.get_json()
    user_email = data.get("email")
    score = data.get("score")
    total = data.get("total", 70)
    percentage = round((score/total)*100, 2)
    passed = percentage >= 85

    results.append({
        "email": user_email,
        "score": score,
        "total": total,
        "percentage": percentage,
        "passed": passed
    })

    return jsonify({
        "message": "Assessment submitted",
        "score": score,
        "percentage": percentage,
        "passed": passed
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

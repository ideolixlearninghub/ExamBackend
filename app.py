from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime
import os

app = Flask(__name__)
CORS(app)

CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)

@app.route("/submit_assessment", methods=["POST"])
def submit_assessment():
    data = request.json
    name = data.get("name", "Student")
    email = data.get("email")
    curriculum = data.get("curriculum", "N/A")
    grade = data.get("grade", "N/A")
    subject = data.get("subject", "N/A")
    assessment_title = data.get("assessment_title", "Assessment")
    score = data.get("score")
    total = data.get("total")

    if email is None or score is None or total is None:
        return jsonify({"error": "Missing required fields"}), 400

    percentage = round((score / total) * 100, 2)
    passed = percentage >= 85

    certificate_link = None

    if passed:
        # Generate certificate PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Header
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width / 2, height - 80, "Ideolix Learning Hub")
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width / 2, height - 130, "Certificate of Achievement")

        # Student Info
        c.setFont("Helvetica", 16)
        c.drawCentredString(width / 2, height - 180, f"Awarded to: {name} ({email})")
        c.drawCentredString(width / 2, height - 210, f"Curriculum: {curriculum} | Grade: {grade}")
        c.drawCentredString(width / 2, height - 240, f"Subject: {subject} | Assessment: {assessment_title}")
        c.drawCentredString(width / 2, height - 270, f"Score: {score}/{total} ({percentage}%)")
        c.drawCentredString(width / 2, height - 300, f"Date: {datetime.date.today().strftime('%B %d, %Y')}")

        # Footer / Congratulations
        c.setFont("Helvetica-Oblique", 16)
        c.drawCentredString(width / 2, height - 360, "Congratulations on your achievement!")

        c.showPage()
        c.save()
        buffer.seek(0)

        # Save PDF
        safe_email = email.replace("@", "_").replace(".", "_")
        filename = f"{CERT_DIR}/{safe_email}_certificate.pdf"
        with open(filename, "wb") as f:
            f.write(buffer.read())

        certificate_link = f"/certificate/{os.path.basename(filename)}"

    return jsonify({
        "percentage": percentage,
        "passed": passed,
        "certificate": certificate_link
    })

@app.route("/certificate/<filename>", methods=["GET"])
def get_certificate(filename):
    path = os.path.join(CERT_DIR, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "Certificate not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

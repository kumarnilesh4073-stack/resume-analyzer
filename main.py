from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "Communication Skills",
    "Teamwork",
    "Basic Computer Knowledge",
    "Customer Handling"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")

    if not file or file.filename == "":
        return "Please select a resume."

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    text = text.lower()

    print("EXTRACTED TEXT:", text)

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    score = int((len(found_skills) / len(SKILLS)) * 100)

    return render_template(
        "result.html",
        filename=file.filename,
        skills=found_skills,
        score=score
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
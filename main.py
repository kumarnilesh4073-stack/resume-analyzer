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
    "Customer Handling",
    "Python",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "Excel",
    "Microsoft Office",
    "Leadership",
    "Problem Solving",
    "Time Management"
]

JOB_ROLES = {
    "Customer Support": [
        "Communication Skills",
        "Customer Handling"
    ],
    "Office Assistant": [
        "Communication Skills",
        "Basic Computer Knowledge",
        "Microsoft Office",
        "Excel"
    ],
    "Team Leader": [
        "Communication Skills",
        "Teamwork",
        "Leadership"
    ],
    "Python Developer": [
        "Python",
        "Problem Solving",
        "Time Management"
    ],
    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Problem Solving"
    ],
    "General Entry Level": [
        "Communication Skills",
        "Teamwork",
        "Basic Computer Knowledge"
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not file or file.filename == "":
        return "Please select a resume."

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        reader = PdfReader(path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    except Exception as e:
        return f"Error reading PDF: {e}"

    text = text.lower()
    job_description = job_description.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    missing_skills = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing_skills.append(skill)

    if len(SKILLS) > 0:
        score = int((len(found_skills) / len(SKILLS)) * 100)
    else:
        score = 0

    strengths = found_skills

    weaknesses = missing_skills

    job_matches = []

    for role, required_skills in JOB_ROLES.items():

        matched = 0

        for skill in required_skills:
            if skill in found_skills:
                matched += 1

        percentage = int(
            (matched / len(required_skills)) * 100
        )

        job_matches.append({
            "role": role,
            "percentage": percentage
        })

    job_required_skills = []

    for skill in SKILLS:
        if skill.lower() in job_description:
            job_required_skills.append(skill)

    job_matched_skills = []

    for skill in job_required_skills:
        if skill in found_skills:
            job_matched_skills.append(skill)

    job_missing_skills = []

    for skill in job_required_skills:
        if skill not in found_skills:
            job_missing_skills.append(skill)

    if len(job_required_skills) > 0:
        job_match = int(
            (len(job_matched_skills) / len(job_required_skills)) * 100
        )
    else:
        job_match = 0

    suggestions = []

    if score < 40:
        suggestions.append(
            "Add more relevant skills to improve your resume score."
        )

    if score >= 40 and score < 70:
        suggestions.append(
            "Your resume is improving. Add more job-related skills."
        )

    if score >= 70:
        suggestions.append(
            "Good resume score. Keep your skills and experience updated."
        )

    if missing_skills:
        suggestions.append(
            "Consider learning some of the missing skills."
        )

    if job_missing_skills:
        suggestions.append(
            "Add relevant skills required by the job description."
        )

    return render_template(
        "result.html",
        filename=file.filename,
        skills=found_skills,
        missing_skills=missing_skills,
        score=score,
        strengths=strengths,
        weaknesses=weaknesses,
        job_matches=job_matches,
        job_match=job_match,
        job_required_skills=job_required_skills,
        job_matched_skills=job_matched_skills,
        job_missing_skills=job_missing_skills,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

from flask import Flask, render_template, request
from analyzer import (
    extract_text_from_pdf,
    calculate_match_score,
    get_missing_skills,
    generate_detailed_report
)

app = Flask(__name__)


def score_section(text, keywords):
    score = 0

    for keyword in keywords:
        if keyword.lower() in text.lower():
            score += 1

    return min(10, score)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    resume_text = extract_text_from_pdf(resume)

    score = calculate_match_score(
        resume_text,
        job_description
    )

    missing_keywords = get_missing_skills(
        resume_text,
        job_description
    )

    skills_score = score_section(
        resume_text,
        [
            "python",
            "java",
            "html",
            "css",
            "sql",
            "flask",
            "react",
            "javascript",
            "c++"
        ]
    )

    project_score = score_section(
        resume_text,
        [
            "project",
            "github",
            "application",
            "system",
            "website",
            "developed"
        ]
    )

    certification_score = score_section(
        resume_text,
        [
            "certificate",
            "certification",
            "course",
            "training"
        ]
    )

    experience_score = score_section(
        resume_text,
        [
            "experience",
            "internship",
            "developer",
            "engineer",
            "worked"
        ]
    )

    suggestions = []

    if score < 50:
        suggestions.append(
            "Add more technical skills mentioned in the Job Description."
        )

    if score < 70:
        suggestions.append(
            "Customize your resume for each job application."
        )

    if len(missing_keywords) > 0:
        suggestions.append(
            "Include the missing keywords naturally in your resume."
        )

    suggestions.append(
        "Add relevant projects with measurable outcomes."
    )

    suggestions.append(
        "Add certifications and training programs."
    )

    suggestions.append(
        "Include GitHub, LinkedIn, or portfolio links."
    )

    suggestions.append(
        "Use action verbs and quantify achievements wherever possible."
    )

    report = generate_detailed_report(
        score,
        missing_keywords
    )

    return render_template(
        "result.html",
        score=score,
        skills_score=skills_score,
        project_score=project_score,
        certification_score=certification_score,
        experience_score=experience_score,
        missing_keywords=missing_keywords,
        suggestions=suggestions,
        report=report,
        resume_text=resume_text[:1000]
    )


if __name__ == "__main__":
    app.run(debug=True)
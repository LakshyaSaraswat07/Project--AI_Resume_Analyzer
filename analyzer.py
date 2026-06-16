import PyPDF2
import re


def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def calculate_match_score(resume_text, job_description):

    stop_words = {
        "the","a","an","and","or","is","are","to","of","for",
        "with","in","on","at","by","from","we","you","our",
        "their","your","will","can","be","this","that",
        "responsibilities","required","looking","strong"
    }

    resume_words = set(
        re.findall(r'\w+', resume_text.lower())
    )

    jd_words = set(
        re.findall(r'\w+', job_description.lower())
    )

    resume_words = resume_words - stop_words
    jd_words = jd_words - stop_words

    if len(jd_words) == 0:
        return 0

    matched = len(
        resume_words.intersection(jd_words)
    )

    score = (matched / len(jd_words)) * 100

    return round(score, 2)


def get_missing_skills(resume_text, job_description):

    stop_words = {
        "the","a","an","and","or","is","are","to","of","for",
        "with","in","on","at","by","from","we","you","our",
        "their","your","will","can","be","this","that",
        "responsibilities","required","looking","strong"
    }

    resume_words = set(
        re.findall(r'\w+', resume_text.lower())
    )

    jd_words = set(
        re.findall(r'\w+', job_description.lower())
    )

    resume_words = resume_words - stop_words
    jd_words = jd_words - stop_words

    missing = jd_words - resume_words

    return sorted(list(missing))[:20]


def generate_detailed_report(
    score,
    missing_keywords
):

    report = []

    if score >= 80:

        report.append(
            "Excellent ATS compatibility."
        )

    elif score >= 60:

        report.append(
            "Good ATS compatibility."
        )

    else:

        report.append(
            "Resume requires improvement."
        )

    if len(missing_keywords) > 0:

        report.append(
            "Several important keywords are missing."
        )

    report.append(
        "Customize your resume according to the job description."
    )

    report.append(
        "Add measurable achievements and projects."
    )

    return report
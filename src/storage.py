import os
import re


def make_safe_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = re.sub(r"\s+", "_", text)
    return text.strip("_")


def save_posting(posting, match):
    os.makedirs("postings", exist_ok=True)

    company = make_safe_filename(posting.company or "Unknown_Company")
    title = make_safe_filename(posting.title or "Unknown_Role")

    filename = f"{company}_{title}.txt"
    output_path = os.path.join("postings", filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Title:    {posting.title}\n")
        f.write(f"Company:  {posting.company}\n")
        f.write(f"Location: {posting.location}\n")
        f.write(f"Type:     {posting.job_type}\n")
        f.write(f"Salary:   {posting.salary}\n")
        f.write(f"URL:      {posting.source_url}\n")

        f.write(f"\nMatch Score: {match['match_score']}%\n")
        f.write(f"Match Reason: {match['reason']}\n")

        f.write("\nSkills:\n")
        for s in posting.skills:
            f.write(f"  - {s}\n")

        f.write("\nResponsibilities:\n")
        for r in posting.responsibilities:
            f.write(f"  - {r}\n")

        f.write("\nQualifications:\n")
        for q in posting.qualifications:
            f.write(f"  - {q}\n")

    return output_path

def save_resume_points(posting, resume_points):
    os.makedirs("resumes", exist_ok=True)

    company = make_safe_filename(posting.company or "Unknown_Company")
    title = make_safe_filename(posting.title or "Unknown_Role")

    filename = f"{company}_{title}_resume_points.txt"
    output_path = os.path.join("resumes", filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(resume_points)

    return output_path
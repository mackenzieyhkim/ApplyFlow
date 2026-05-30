import os
import re
from dotenv import load_dotenv
from src.classifier import classify_job_description, score_job_match

load_dotenv()


def make_safe_filename(text):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = re.sub(r"\s+", "_", text)
    return text.strip("_")


def save_posting(posting, match):
    os.makedirs("outputs", exist_ok=True)

    company = make_safe_filename(posting.company or "Unknown_Company")
    title = make_safe_filename(posting.title or "Unknown_Role")
    filename = f"{company}_{title}.txt"
    output_path = os.path.join("outputs", filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Title:    {posting.title}\n")
        f.write(f"Company:  {posting.company}\n")
        f.write(f"Location: {posting.location}\n")
        f.write(f"Type:     {posting.job_type}\n")
        f.write(f"Salary:   {posting.salary}\n")
        f.write(f"URL:      {posting.source_url}\n")

        f.write(f"\nMatch Score: {match['match_score']}%\n")
        f.write(f"Match Reason: {match['reason']}\n")

        f.write(f"\nSkills:\n")
        for s in posting.skills:
            f.write(f"  - {s}\n")

        f.write(f"\nResponsibilities:\n")
        for r in posting.responsibilities:
            f.write(f"  - {r}\n")

        f.write(f"\nQualifications:\n")
        for q in posting.qualifications:
            f.write(f"  - {q}\n")

    return output_path


def main():
    print("AI Job Filtering System")

    url = input("Paste a job posting link: ").strip()

    try:
        print("\nFetching and classifying job posting...")
        posting = classify_job_description(url)

        print("Scoring against profile...")
        match = score_job_match(posting)

        print(f"\nMatch Score: {match['match_score']}%")
        print(f"Reason:      {match['reason']}")

        output_path = save_posting(posting, match)
        print(f"\nSaved to: {output_path}")
        print("Done.")

    except Exception as error:
        print("\nSomething went wrong while processing:")
        print(error)


if __name__ == "__main__":
    main()


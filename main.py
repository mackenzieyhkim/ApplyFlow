from dotenv import load_dotenv
from src.classifier import classify_job_description, score_job_match
from src.storage import save_posting

load_dotenv()


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
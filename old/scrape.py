import requests
import trafilatura


def fetch_job_text(url: str) -> str:
    """
    Downloads a webpage and extracts the main readable text.
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    extracted_text = trafilatura.extract(response.text)

    if not extracted_text:
        raise ValueError("Could not extract readable job text from this page.")

    return extracted_text


import json
import re
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.model import Posting

load_dotenv()
client = genai.Client(api_key=os.getenv("KEY_TO_EMPLOYMENT"))

CLASSIFY_PROMPT = """Visit this job posting URL and extract key info. Return ONLY valid JSON, no markdown, no explanation.

URL: {url}

{{
  "title": "job title or null",
  "company": "company name or null",
  "location": "location or null",
  "responsibilities": ["up to 5 most important"],
  "qualifications": ["up to 5 most important"],
  "skills": ["up to 8 skills"],
  "salary": "salary string or null",
  "job_type": "Full-time | Part-time | Internship | Co-op or null"
}}"""

SCORE_PROMPT = """Given this candidate profile and job posting, return ONLY valid JSON, no markdown, no explanation.

{{
  "match_score": <integer 0-100>,
  "reason": "2-3 sentence explanation of why this is or isn't a good fit"
}}

CANDIDATE PROFILE:
{profile}

JOB POSTING:
Title: {title}
Company: {company}
Skills Required: {skills}
Qualifications: {qualifications}
Responsibilities: {responsibilities}
"""

RESUME_PROMPT = """
You are an expert resume writer.

Using the candidate profile and job posting below:

1. Select the 3 most relevant experiences and 2 most relevant projects.
2. Rewrite each experience into 3 ATS optimized bullet points.
3. Use keywords from the job posting naturally.
4. Do not invent experience.
5. Quantify achievements where possible.

Return plain text only.

CANDIDATE PROFILE:
{profile}

JOB POSTING:
Title: {title}
Company: {company}

Skills:
{skills}

Qualifications:
{qualifications}

Responsibilities:
{responsibilities}
"""


def classify_job_description(url: str) -> Posting:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=CLASSIFY_PROMPT.format(url=url),
        config=types.GenerateContentConfig(
            tools=[types.Tool(url_context=types.UrlContext())]
        )
    )

    raw = re.sub(r"```json|```", "", response.text).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Warning: could not parse Gemini response as JSON")
        print("Raw response:", raw)
        data = {}

    return Posting(
        source_url=url,
        full_description=raw,
        title=data.get("title"),
        company=data.get("company"),
        location=data.get("location"),
        responsibilities=data.get("responsibilities", []),
        qualifications=data.get("qualifications", []),
        skills=data.get("skills", []),
        salary=data.get("salary"),
        job_type=data.get("job_type"),
    )


def score_job_match(posting: Posting, profile_path: str = "profile.txt") -> dict:
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = f.read()
    except FileNotFoundError:
        print(f"Warning: profile file not found at '{profile_path}', skipping score.")
        return {"match_score": None, "reason": "Profile not found."}

    prompt = SCORE_PROMPT.format(
        profile=profile,
        title=posting.title or "Unknown",
        company=posting.company or "Unknown",
        skills=", ".join(posting.skills),
        qualifications=", ".join(posting.qualifications),
        responsibilities=", ".join(posting.responsibilities),
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    raw = re.sub(r"```json|```", "", response.text).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("Warning: could not parse score response as JSON")
        print("Raw response:", raw)
        return {"match_score": None, "reason": "Could not parse score."}
    
def generate_resume_points(posting: Posting, profile_path: str = "profile.txt") -> str:
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = f.read()
    except FileNotFoundError:
        return "Profile not found. Could not generate resume points."

    prompt = RESUME_PROMPT.format(
        profile=profile,
        title=posting.title or "Unknown",
        company=posting.company or "Unknown",
        skills=", ".join(posting.skills),
        qualifications=", ".join(posting.qualifications),
        responsibilities=", ".join(posting.responsibilities),
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text
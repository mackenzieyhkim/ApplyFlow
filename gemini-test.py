import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("KEY_TO_EMPLOYMENT"))

PROMPT = """ visit this site and list all the postings available
URL: {url}
"""

def prompt(url: str):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=PROMPT.format(url=url),
        config=types.GenerateContentConfig(
            tools=[types.Tool(url_context=types.UrlContext())]
        )
    )

    print(response.text)

url = input("Enter URL: ")
prompt(url)


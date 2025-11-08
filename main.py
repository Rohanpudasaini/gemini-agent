import os
import sys

from dotenv import load_dotenv
from google import genai

args = sys.argv[1:]
if not args:
    raise ValueError("Please provide at least one argument.")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
prompt = args[0]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
)
print("Response:", response.text)
print("usages", response.usage_metadata)

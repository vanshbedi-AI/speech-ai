import json
import os

from groq import Groq
from dotenv import load_dotenv
from prompts import SUMMARY_PROMPT

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

print("API Key Exists:", api_key is not None)

if not api_key:
    raise Exception("GROQ_API_KEY environment variable not found")

client = Groq(api_key=api_key)


class MeetingSummarizer:

    def summarize(self, transcript):

        prompt = SUMMARY_PROMPT.format(
            transcript=transcript
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        output = response.choices[0].message.content

        if output.startswith("```"):
            output = output.replace("```json", "").replace("```", "").strip()

        return json.loads(output)
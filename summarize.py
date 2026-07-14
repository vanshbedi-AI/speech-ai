import json
import os

from groq import Groq
from dotenv import load_dotenv

from prompts import SUMMARY_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class MeetingSummarizer:

    def summarize(self, transcript):

        prompt = SUMMARY_PROMPT.format(
            transcript=transcript
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"system",
                    "content":"Return valid JSON only."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0
        )

        output = response.choices[0].message.content

        return json.loads(output)
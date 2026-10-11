import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

system_prompt = """
You should only and only answer coding related questions.
Do not answer anything else.
If user asks something other than coding, just say sorry.
"""

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": "Can you tell me a joke?",
        },
        {
            "role": "user",
            "content": "Can you translate the word hello to French??",
        },
        {
            "role": "user",
            "content": "Can you write a Python code to translate?",
        }
    ],
)

print(response.choices[0].message.content)



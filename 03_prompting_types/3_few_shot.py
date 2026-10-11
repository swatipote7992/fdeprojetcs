import os

import json
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

Rules:
- Strictly follow the output in JSON format.

Output format:
{"code": string or null, "is_coding_question": boolean}

Examples:
Q: Can you explain the (a + b) whole square?
A: {"code": null, "is_coding_question": false}

Q: Write a function to add two numbers in Python.
A: {"code": "def add(a, b):\\n    return a + b", "is_coding_question": true}

"""

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": "Can you write a Python code to multiply two numbers?",
        },
    ],
)

result = json.loads(response.choices[0].message.content)
print(result["code"])
print(result["is_coding_question"])

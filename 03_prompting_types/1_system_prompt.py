import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in maths and only answer maths-related questions. If the query is not related to maths, just say sorry and do not answer.",
        },
        {
            "role": "user",
            "content": "Hey, I am user, nice to meet you",
        },
        {
            "role": "user",
            "content": "Can you help me solve (a + b) whole squared?",
        },
    ],
)

print(response.choices[0].message.content)

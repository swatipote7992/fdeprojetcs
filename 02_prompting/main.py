from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello, I am Guest ! Nice to meet you. Can you tell me a joke?"}
    ]
)

print(response.choices[0].message.content)

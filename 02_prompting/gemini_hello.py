from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Hello, I am Guest ! Nice to meet you. Can you tell me a joke?",
)

print(response.text)
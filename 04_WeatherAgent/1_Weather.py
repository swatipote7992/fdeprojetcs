from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()
client = OpenAI()

system_prompt = """
You are an expert Weather Agent. 
You will answer questions related to weather, climate, and meteorology using chain of thought reasoning.
If user asks something other than weather, climate, or meteorology, politely say that you only answer questions related to weather.
You work in stpes: START, PLAN and OUTPUT
First plan what needs to be done. The plan can be multiple steps.
Once enough planning is done, give the output.

Rules:
- Strictly follow the output in JSON format.
- Run one step at a time.
- The sequence of steps is start (user input), plan (can repeat), tool (if needed), observe, output.

Output JSON format:
{"step": "start" | "plan" | "output", "content": "string"}

Example:
Start: What is the weather in London today?
Plan: { "step": "plan", "content": "The user is asking about the current weather in London."}
Plan: { "step": "plan", "content": "I need to provide the current weather conditions in London, including temperature, humidity, and precipitation."}
Output: { "step": "output", "content": "The current weather in London is 15°C with light rain."}
"""

message_history = [
    {"role": "system", "content": system_prompt},
]


user_input = input("Enter your query: ")
message_history.append({"role": "user", "content": user_input}) 

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format = { "type": "json_object"},
        messages= message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)
    step = parsed_result.get("step")

    if step == "start":
        print("🔥", parsed_result.get("content"))
        continue
    if step == "plan":
        print("🧠", parsed_result.get("content"))
        continue
    if step == "output":
        print("✅", parsed_result.get("content"))
        break
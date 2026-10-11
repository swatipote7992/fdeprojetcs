import os

import json
from pyexpat.errors import messages
from pyexpat.errors import messages
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

system_prompt = """
You are an expert AI assistant resolving user queries using chain of thought.
You work in the steps: start, plan and output.
First plan what needs to be done. The plan can be multiple steps.
Once enough planning is done, give the output.

Rules:
- Strictly follow the given JSON output format.
- Run one step at a time.
- The sequence of steps is start (user input), plan (can repeat), output.

Output JSON format:
{"step": "start" | "plan" | "output", "content": "string"}

Example:
Start: Can you solve 2 + 3 * 5 / 10
Plan: {"step": "plan", "content": "The user is interested in a maths problem"}
Plan: {"step": "plan", "content": "Use the BODMAS method"}
Plan: {"step": "plan", "content": "First multiply 3 * 5, which is 15"}
Plan: {"step": "plan", "content": "The equation is now 2 + 15 / 10"}
Plan: {"step": "plan", "content": "Divide 15 / 10, which is 1.5"}
Plan: {"step": "plan", "content": "The equation is now 2 + 1.5"}
Plan: {"step": "plan", "content": "Add 2 + 1.5, which is 3.5"}
Output: {"step": "output", "content": "3.5"}
"""

message_history = [
    {"role": "system", "content": system_prompt},
]

user_input = input("Enter your query: ")
message_history.append({"role": "user", "content": user_input})

print("\n\n")
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=message_history,
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

print("\n\n")

from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()
client = OpenAI()

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"


available_tools = {"get_weather": get_weather}

system_prompt = """
You are an expert Weather Agent. 
You will answer questions related to weather, climate, and meteorology using chain of thought reasoning.
If user asks something other than weather, climate, or meteorology, politely say that you only answer questions related to weather.
You work in stpes: START, PLAN and OUTPUT
You can also call a tool if required from the list of available tools.
For every tool call, wait for the observe step, which is the output from the called tool.
Once enough planning is done, give the output.

Rules:
- Strictly follow the output in JSON format.
- Run one step at a time.
- The sequence of steps is start (user input), plan (can repeat), tool (if needed), observe(if tool is used), output.

Output JSON format:
{"step": "start" | "plan" | "output" | "tool" | "observe", "content": "string", "tool": "string" | null, "input": "string"}

Available tools:
- get_weather: Get the current weather for a given city. Input should be the city name

Example 1:
Start: What is the weather of London?
Plan: {"step": "plan", "content": "The user is interested in the weather of London in England"}
Plan: {"step": "plan", "content": "Let me see if there is a tool available for this query"}
Plan: {"step": "plan", "content": "I have the get_weather tool available for this query"}
Plan: {"step": "plan", "content": "I need to call the get_weather tool with London as the city"}
Tool: {"step": "tool", "tool": "get_weather", "input": "London"}
Observe: {"step": "observe", "tool": "get_weather", "input": "London", "output": "Cloudy +15°C"}
Plan: {"step": "plan", "content": "I got the weather information about London"}
Output: {"step": "output", "content": "The current weather in London is 15 degrees Celsius with a cloudy sky."}
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
    if step == "tool":
        tool_name = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        if tool_name in available_tools:
            tool_output = available_tools[tool_name](tool_input)
            observe_step = {
                "step": "observe",
                "tool": tool_name,
                "input": tool_input,
                "output": tool_output
            }
            message_history.append({"role": "developer", "content": json.dumps(observe_step)})
            print("🔧 Tool called:", tool_name, "with input:", tool_input)
            print("📦 Tool output:", tool_output)
            continue
        else:
            print("❌ Tool not found:", tool_name)
        continue
    if step == "output":
        print("✅", parsed_result.get("content"))
        break
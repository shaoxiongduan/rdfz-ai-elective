from openai import OpenAI

base_url = "https://pro.aiskt.com/v1"
api_key = "Your-API-Key"

client = OpenAI(base_url=base_url, api_key=api_key)

system_prompt = (
    "You are a helpful assistant that can answer questions and help with tasks."
)

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
]


user_input = "hello world"

messages.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.5
)

assistant_message = response.choices[0].message.content
print(f"Assistant: {assistant_message}")

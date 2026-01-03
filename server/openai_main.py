from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages= [
        {"role": "user", "content": "Hey There"} 
    ]
)

print(response.choices[0].message.content)
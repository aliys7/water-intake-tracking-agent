import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def get_openrouter_response(prompt, model="qwen/qwen-max", temperature=0.9, max_tokens=300):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": "http://localhost:8501",  
                "X-Title": "Water Intake Tracker" 
            }
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return "API Error: Check your configuration."
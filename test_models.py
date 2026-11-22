from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

models = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]

for model in models:
    try:
        client.models.generate_content(model=model, contents="Say hi")
        print("CALISIYOR:", model)
    except Exception as e:
        print("HATA:", model, "-", str(e)[:80])
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client()

for attempt in range(1, 6):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="What is the best bank account for expats living in Germany?",
        )
        print(response.text)
        break
    except errors.ServerError:
        print(f"Model yoğun (deneme {attempt}/5). 10 saniye bekleniyor...")
        time.sleep(10)
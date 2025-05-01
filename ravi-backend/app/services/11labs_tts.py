#sk_b202f6ad0725fd19e623700a7dd290f81a2a6606c31fd7b0 > haffaomer22@gmail.com

import requests

API_KEY = "sk_b202f6ad0725fd19e623700a7dd290f81a2a6606c31fd7b0"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "text": "السلام علیکم! یہ ElevenLabs کی اردو ٹیکسٹ ٹو اسپیچ سروس کا ایک ڈیمو ہے۔",
    "model_id": "eleven_multilingual_v1",
    "voice_settings": {
        "stability": 0.7,           # smoother speech
        "similarity_boost": 0.85    # closer to the original voice tone
    }
}

response = requests.post(url, headers=headers, json=data)

# Save the audio file
with open("urdu_output.mp3", "wb") as f:
    f.write(response.content)

print("✅ Urdu speech generated and saved as urdu_output.mp3")



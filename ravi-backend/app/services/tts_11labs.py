import requests

API_KEY = ""
VOICE_ID = ""  

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "text": "آپ کیسے ہیں",
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

print("Urdu speech generated and saved as urdu_output.mp3")



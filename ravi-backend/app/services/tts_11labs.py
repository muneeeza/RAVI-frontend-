import requests

from app.services.tts import TTSService
from app.config import settings

class ElevenLabsTTSService(TTSService):
    def __init__(self):
        self.API_KEY            = settings.ELEVENLABS_API_KEY

        self.MODEL_ID           = settings.MODEL_ID
        self.VOICE_ID           = settings.VOICE_ID
        self.VOICE_SETTINGS     = settings.VOICE_SETTINGS

        self.URL                = f"https://api.elevenlabs.io/v1/text-to-speech/{self.VOICE_ID}"

    def synthesize(self, text: str = "آپ کیسے ہیں") -> bytes:
        
        headers = {
            "xi-api-key": self.API_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "model_id": self.MODEL_ID,
            "voice_settings": self.VOICE_SETTINGS
        }
        
        response = requests.post(self.URL, headers=headers, json=data)

        # Save the audio file
        with open("urdu_output.mp3", "wb") as f:
            f.write(response.content)

        print("Urdu speech generated and saved as urdu_output.mp3")

        return response.content


haffu = ElevenLabsTTSService()

haffu.synthesize("آپ کیسے ہیں")
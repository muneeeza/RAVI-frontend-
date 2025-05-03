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

        if not response.ok:
            # print("TTS API Error:", response.status_code, response.text)
            raise RuntimeError(f"TTS API failed: {response.status_code}")

        content_type = response.headers.get("Content-Type", "")
        if "audio" not in content_type:
            # print("Expected audio but got:", content_type)
            # print(response.text)  # Probably a text-based error or warning
            raise RuntimeError("Expected audio response but got non-audio data")

        # Save the audio file
        with open("urdu_output.mp3", "wb") as f:
            f.write(response.content)
        
        # print("Audio saved to debug.mp3 (length:", len(response.content), "bytes)")

        return response.content
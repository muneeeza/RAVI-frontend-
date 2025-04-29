import os

class Settings:
    GCP_CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    TTS_VOICE = os.getenv("TTS_VOICE", "ur-PK-Wavenet-B")
    TTS_AUDIO_ENCODING = os.getenv("TTS_AUDIO_ENCODING", "MP3")
    TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "ur-PK")

settings = Settings()
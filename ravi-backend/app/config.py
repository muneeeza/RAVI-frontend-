import os, yaml

class Settings:
    def __init__(self, path: str = "config.yaml"):
        with open(path, "r") as f:
            cfg = yaml.safe_load(f)

        # OCR
        o = cfg.get("ocr", {})
        self.OCR_ENGINE         = o.get("engine", "tesseract")
        self.TESSERACT_CMD      = o.get("tesseract_cmd", None)
        self.OCR_LANG           = o.get("lang", "urd")
        self.OCR_MODEL_PATH     = o.get("model_path", None)
        self.EASYOCR_GPU        = o.get("gpu", False)

        # TTS
        t = cfg.get("tts", {})
        self.VOICE_ID           = t.get("voice_id", "ur-PK-Wavenet-B")
        self.LANGUAGE           = t.get("language", "ur-PK")
        self.AUDIO_ENCODING     = t.get("audio_encoding", "MP3")
        self.MODEL_ID           = t.get("model_id", "eleven_multilingual_v1")
        self.VOICE_SETTINGS     = t.get("voice_settings", {"stability": 0.7, "similarity_boost": 0.85})

        with open("secrets.yaml", "r") as f:
            secrets = yaml.safe_load(f)

        self.ELEVENLABS_API_KEY = secrets.get("api", {}).get("key")


settings = Settings(os.getenv("CONFIG_PATH", "config.yaml"))
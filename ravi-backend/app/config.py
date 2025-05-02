import os, yaml

class Settings:
    def __init__(self, path: str = "config.yaml"):
        with open(path, "r") as f:
            cfg = yaml.safe_load(f)

        # OCR
        o = cfg.get("ocr", {})
        self.OCR_ENGINE      = o.get("engine", "tesseract")
        self.TESSERACT_CMD   = o.get("tesseract_cmd", None)
        self.OCR_LANG        = o.get("lang", "urd")
        self.OCR_MODEL_PATH  = o.get("model_path", None)
        self.EASYOCR_GPU     = o.get("gpu", False)

        # TTS
        t = cfg.get("tts", {})
        self.TTS_VOICE       = t.get("voice", "ur-PK-Wavenet-B")
        self.TTS_LANGUAGE    = t.get("language", "ur-PK")
        self.TTS_AUDIO_ENCODING = t.get("audio_encoding", "MP3")

        # GCP
        self.GCP_CREDENTIALS_JSON = cfg.get("gcp_credentials") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

settings = Settings(os.getenv("CONFIG_PATH", "config.yaml"))
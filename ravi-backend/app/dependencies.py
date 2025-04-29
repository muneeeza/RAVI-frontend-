from fastapi import Depends
from app.services.ocr import LocalOCREngine, OCRService
from app.services.tts import TTSService

# You could read MODEL_PATH from config or env
OCR_MODEL_PATH = "/path/to/your/ocr/model"

def get_ocr_service() -> OCRService:
    return LocalOCREngine(model_path=OCR_MODEL_PATH)

def get_tts_service() -> TTSService:
    return TTSService()

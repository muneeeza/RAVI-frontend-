from app.config import settings
from app.services.ocr_tesseract import TesseractOCREngine
from app.services.ocr_easyocr import EasyOCREngine
from app.services.ocr import LocalOCREngine, OCRService
from app.services.tts import TTSService

def get_ocr_service() -> OCRService:
    engine = settings.OCR_ENGINE.lower()
    if engine == "tesseract":
        return TesseractOCREngine(
            tesseract_cmd=settings.TESSERACT_CMD,
            lang=settings.OCR_LANG,
        )
    elif engine == "easyocr":
        return EasyOCREngine(
            gpu=settings.EASYOCR_GPU
        )
    elif engine == "custom":
        if not settings.OCR_MODEL_PATH:
            raise RuntimeError("OCR_MODEL_PATH not set for custom engine")
        return LocalOCREngine(model_path=settings.OCR_MODEL_PATH)
    else:
        raise RuntimeError(f"Unsupported OCR engine: {engine}")

def get_tts_service() -> TTSService:
    # ensure GCP creds are loaded
    if settings.GCP_CREDENTIALS_JSON:
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GCP_CREDENTIALS_JSON
    return TTSService(
        language=settings.TTS_LANGUAGE,
        voice=settings.TTS_VOICE,
        audio_encoding=settings.TTS_AUDIO_ENCODING,
    )

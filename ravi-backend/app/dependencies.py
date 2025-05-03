from app.config import settings
from app.services.ocr_tesseract import TesseractOCREngine
from app.services.ocr_easyocr import EasyOCREngine
from app.services.ocr_local import LocalOCREngine
from app.services.ocr import OCRService
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
    if settings.MODEL_ID == "eleven_multilingual_v1":
        from app.services.tts_11labs import ElevenLabsTTSService
        return ElevenLabsTTSService()
    else:
        raise RuntimeError(f"Unsupported TTS model: {settings.MODEL_ID}")
    

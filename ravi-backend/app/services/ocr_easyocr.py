import io
from PIL import Image
import easyocr
from app.services.ocr import OCRService

class EasyOCREngine(OCRService):
    def __init__(self, gpu=False):
        self.reader = easyocr.Reader(["ur"], gpu=gpu)

    def extract_text(self, image_bytes: bytes) -> str:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        results = self.reader.readtext(img)
        return " ".join([r[1] for r in results])

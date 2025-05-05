import io
from PIL import Image
import pytesseract
import unicodedata

from app.services.ocr import OCRService

class TesseractOCREngine(OCRService):
    def __init__(self, tesseract_cmd=None, lang="urd"):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def extract_text(self, image_bytes: bytes) -> str:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        text = pytesseract.image_to_string(img, config='-l urd --psm 6')
        text = text.replace('\n','').strip()
        
        text = unicodedata.normalize("NFC", text)

        return text
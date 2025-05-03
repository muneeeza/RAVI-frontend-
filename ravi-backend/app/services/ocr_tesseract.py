import io
from PIL import Image
import pytesseract
import arabic_reshaper
from bidi.algorithm import get_display
import unicodedata

from app.services.ocr import OCRService

class TesseractOCREngine(OCRService):
    def __init__(self, tesseract_cmd=None, lang="urd"):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def extract_text(self, image_bytes: bytes) -> str:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        raw = pytesseract.image_to_string(img, config='-l urd --psm 6')
        raw = raw.replace('\n','').strip()

        # 1) Arabic‐reshape: picks correct contextual glyphs
        # reshaped = arabic_reshaper.reshape(raw)

        # 2) BiDi reorder: make it display right-to-left
        # display_text = get_display(reshaped)
        # display_text = get_display(raw)

        # display_text = unicodedata.normalize("NFC", display_text)
        # return display_text
        
        raw = unicodedata.normalize("NFC", raw)

        return raw
import  io
import  numpy as np
from    PIL import Image
import  tensorflow as tf

from app.services.ocr import OCRService
from app.services.ocr import index_to_char


class LocalOCREngine(OCRService):
    def __init__(self, model_path: str, img_height=128, img_width=128):
        self.img_height = img_height
        self.img_width = img_width
        self.model = tf.keras.models.load_model(model_path, compile=False)

    def _preprocess(self, image_bytes: bytes) -> tf.Tensor:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((self.img_width, self.img_height), Image.BILINEAR)
        arr = np.array(img).astype(np.float32) / 255.0
        return tf.expand_dims(arr, axis=0)  # shape: (1, H, W, 3)

    def extract_text(self, image_bytes: bytes) -> str:
        input = self._preprocess(image_bytes)                 # shape (1,H,W,3)
        logits = self.model.predict(input)                    # (1, T, C)

        chars = [index_to_char[idx] for idx in logits if idx > 0]
        # text  = np.argmax(logits, axis=2)[0]
        text  = "".join(chars)

        return text

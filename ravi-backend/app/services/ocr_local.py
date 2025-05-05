import io
from PIL import Image
from app.services.ocr import OCRService
import tensorflow as tf
import numpy as np
from app.services.ocr import index_to_char

# class LocalOCREngine(OCRService):
#     def __init__(self, model_path: str):
#         # load your OCR model here (e.g. TensorFlow/Keras, PyTorch, etc.)
#         # self.model = load_model(model_path)
#         self.model_path = model_path

#     def extract_text(self, image_bytes: bytes) -> str:
#         # convert bytes -> image array, preprocess, run inference
#         # e.g.:
#         # img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         # text = self.model.predict(img)
#         # return text
#         raise NotImplementedError("Hook in your own inference code")



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

    # def _ctc_greedy_decode(self, logits: np.ndarray) -> str:
    #     """
    #     logits: (1, time_steps, num_classes)
    #     returns: decoded UTF-8 string
    #     """
    #     # Transpose to time-major for tf.nn.ctc_greedy_decoder
    #     time_major = tf.transpose(logits, [1, 0, 2])
    #     # All sequences are full-length
    #     seq_len = tf.fill([1], time_major.shape[0])
    #     # Perform greedy CTC decoding
    #     decoded, _ = tf.nn.ctc_greedy_decoder(time_major, seq_len)
    #     dense = tf.sparse.to_dense(decoded[0], default_value=0).numpy().flatten()
    #     # Map indices → chars, skipping blanks (0)


    def extract_text(self, image_bytes: bytes) -> str:
        # 1) Preprocess into model-ready tensor
        input = self._preprocess(image_bytes)                 # shape (1,H,W,3)
        # 2) Run through network to get softmax logits
        logits = self.model.predict(input)                    # (1, T, C)

        chars = [index_to_char[idx] for idx in logits if idx > 0]
        # text  = np.argmax(logits, axis=2)[0]
        text  = "".join(chars)

        return text

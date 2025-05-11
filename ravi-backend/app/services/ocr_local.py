import io
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import torch

import logging
logging.getLogger('tensorflow').disabled = True

from app.services.ocr import OCRService

from app.services.helper import binarize_image, index_to_char, characters


class LocalOCREngine(OCRService):
    def __init__(self, model_path: str, img_height=32, img_width=128):
        self.img_height = img_height
        self.img_width = img_width
        self.model_path = model_path

        ext = os.path.splitext(model_path)[1].lower()
        self.model_type = None

        if ext == '.h5':
            self.image_height = 128
            self.model_type = 'tensorflow'
            self.model = tf.keras.models.load_model(model_path, compile=False)
        elif ext == '.pth':
            self.model_type = 'pytorch'
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = load_model(self.model_path, num_classes=len(characters), device=self.device)
        else:
            raise ValueError(f"Unsupported model extension: {ext}")

    def extract_text(self, image_bytes: bytes) -> str:

        if self.model_type == 'tensorflow':
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = img.resize((self.img_width, self.img_height), Image.BILINEAR)
            arr = np.array(img).astype(np.float32) / 255.0  # Normalize to [0,1]
            input_tensor = tf.expand_dims(arr, axis=0)  # shape (1,H,W,3)
            logits = self.model.predict(input_tensor)   # (1, T, C)
            output = np.argmax(logits, axis=2)[0]
            chars = [index_to_char[idx] for idx in output if idx > 0]
            return "".join(chars)

        elif self.model_type == 'pytorch':
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            recognized_text = recognize_text(image, self.model, self.device, index_to_char, binarize_method='sauvola')
            return recognized_text
        else:
            raise RuntimeError("Model type not supported or not loaded.")


# import  io
# import  numpy as np
# from    PIL import Image
# import  tensorflow as tf

# import  logging
# logging.getLogger('tensorflow').disabled = True

# from app.services.ocr import OCRService
# from app.services.ocr import index_to_char


# class LocalOCREngine(OCRService):
#     def __init__(self, model_path: str, img_height=128, img_width=128):
#         self.img_height = img_height
#         self.img_width = img_width
#         self.model = tf.keras.models.load_model(model_path, compile=False)

#     def _preprocess(self, image_bytes: bytes) -> tf.Tensor:
#         img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         img = img.resize((self.img_width, self.img_height), Image.BILINEAR)
#         arr = np.array(img).astype(np.float32) / 255.0
#         return tf.expand_dims(arr, axis=0)  # shape: (1, H, W, 3)

#     def extract_text(self, image_bytes: bytes) -> str:
#         input = self._preprocess(image_bytes)                 # shape (1,H,W,3)
#         logits = self.model.predict(input)                    # (1, T, C)

#         output  = np.argmax(logits, axis=2)[0]
#         chars = [index_to_char[idx] for idx in output if idx > 0]
#         text  = "".join(chars)

#         return text


import torch.nn as nn
class UrduCRNN(nn.Module):
    def __init__(self, num_classes):
        super(UrduCRNN, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, None))  # force height = 1
        )
        self.rnn = nn.LSTM(
            input_size=256,  # final channel depth after CNN
            hidden_size=256,
            bidirectional=True,
            num_layers=2
        )
        self.fc = nn.Linear(512, num_classes)  # 256 * 2 for BiLSTM

    def forward(self, x):
        # x: [B, 1, H, W]
        x = self.cnn(x)  # [B, 256, 1, W]
        x = x.squeeze(2)  # [B, 256, W]
        x = x.permute(2, 0, 1)  # [W, B, 256]
        x, _ = self.rnn(x)  # [W, B, 512]
        x = self.fc(x)  # [W, B, num_classes]
        return x

def recognize_text(image, model, device, index_to_char, binarize_method=None):
    """
    Recognize text in an image using the trained OCR model.
    
    Args:
        image_path: Path to the input image
        model: Trained CRNN model
        device: Torch device (CPU or GPU)
        index_to_char: Dictionary mapping from indices to characters
    
    Returns:
        Recognized text string
    """
    from PIL import Image
    import torch
    import torch.nn.functional as F
    import torchvision.transforms as T
    
    # Create the same transform as used during training
    transform = T.Compose([
        T.Grayscale(),
        T.Resize((32, 128)),  # height=32
        T.ToTensor(),
        T.Normalize((0.5,), (0.5,))  # Important: match your training normalization
    ])
    
    # Apply binarization if specified
    # if binarize_method:
    #     image = binarize_image(image, method=binarize_method)

    # Open and transform the image
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    image_tensor = image_tensor.to(device)
    
    # Set model to evaluation mode
    model.eval()
    
    with torch.no_grad():
        # Forward pass
        logits = model(image_tensor)
        
        # Apply softmax to get probabilities
        log_probs = F.log_softmax(logits, dim=2)
        
        # Greedy decoding (take most likely character at each position)
        pred = log_probs.argmax(dim=2)
        pred = pred.transpose(1, 0).contiguous().view(-1)
        
        # Convert to labels
        pred_list = []
        prev = -1  # To handle CTC duplicate removal
        
        for i in range(len(pred)):
            if pred[i] != 0 and pred[i] != prev:  # Skip blank (0) and duplicates
                pred_list.append(index_to_char[pred[i].item()])
            prev = pred[i]
        
        # Join characters to form the predicted text
        predicted_text = ''.join(pred_list)
        
    return predicted_text

# Load your trained model
def load_model(model_path, num_classes, device):
    """
    Load the trained OCR model.
    
    Args:
        model_path: Path to the saved model weights
        num_classes: Number of character classes
        device: Torch device (CPU or GPU)
    
    Returns:
        Loaded model
    """
    import torch
    
    model = UrduCRNN(num_classes=num_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model
        
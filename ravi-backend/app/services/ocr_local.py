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
            self.model_type = 'tensorflow'
            self.device = "/GPU:0" if tf.config.list_physical_devices('GPU') else "/CPU:0"
            self.model = tf.keras.models.load_model(model_path, compile=False)
        elif ext == '.pth':
            self.model_type = 'pytorch'
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = load_model(self.model_path, num_classes=len(characters), device=self.device)
        else:
            raise ValueError(f"Unsupported model extension: {ext}")

    def extract_text(self, image_bytes: bytes) -> str:

        if self.model_type == 'tensorflow':
            image = Image.open(io.BytesIO(image_bytes)).convert("L")
            recognized_text = recognize_tf_text(image=image, model=self.model, index_to_char=index_to_char, image_height=self.img_height, image_width=self.img_width)
            return recognized_text

        elif self.model_type == 'pytorch':
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            recognized_text = recognize_text(image, self.model, self.device, index_to_char, binarize_method='sauvola')
            return recognized_text
        else:
            raise RuntimeError("Model type not supported or not loaded.")


def preprocess_image(image, target_width=128, target_height=32):
    """
    Standardized preprocessing for OCR images

    Args:
        image: Either a file path or a PIL Image object
        target_width: Width to resize to
        target_height: Height to resize to

    Returns:
        Preprocessed numpy array ready for model prediction
    """
    # Handle both file paths and PIL Image objects
    if isinstance(image, str):
        # It's a file path
        img = Image.open(image).convert('L')
    else:
        # It's already a PIL Image object
        img = image.convert('L')  # Ensure grayscale

    # Resize with consistent method
    img = img.resize((target_width, target_height), Image.BILINEAR)

    # Convert to numpy array and normalize
    img_array = np.array(img).astype(np.float32) / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

#    # Ensure proper shape (batch, height, width, channels)
#    if len(img_array.shape) == 3:  # (batch, height, width)
#         img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
    
    return img_array

# Function to recognize text in an image
def recognize_tf_text(image, model, index_to_char, image_height=32, image_width=128):
    img_array = preprocess_image(image, target_width=image_width, target_height=image_height)
    
    # Get prediction
    prediction = model.predict(img_array, verbose=0)
    
    # Decode prediction (greedy)
    indices = np.argmax(prediction[0], axis=1)
    
    # Merge repeated characters
    merged = []
    prev = -1
    for idx in indices:
        if idx != prev and idx != 0:  # Skip blanks and repeats
            merged.append(idx)
        prev = idx
    
    # Convert indices to characters
    text = ''.join([index_to_char[int(idx)] for idx in merged])
    return text


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
        
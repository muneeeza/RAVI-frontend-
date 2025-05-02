from abc import ABC, abstractmethod

urdu_chars = [
    'ا', 'ب', 'پ', 'ت', 'ٹ', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ڈ', 'ذ', 'ر', 'ڑ',
    'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل',
    'م', 'ن', 'و', 'ہ', 'ء', 'ی', 'آ'
]

# Create index mapping
char_to_index = {char: idx + 1 for idx, char in enumerate(urdu_chars)}
index_to_char = {idx: char for char, idx in char_to_index.items()}

"""
The abstract class
"""
class OCRService(ABC):
    
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        ...
from abc import ABC, abstractmethod

"""
The abstract class
"""
class OCRService(ABC):
    
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        ...
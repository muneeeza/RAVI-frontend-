from abc import ABC, abstractmethod
from app.config import settings

class TTSService(ABC):
    
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        ...

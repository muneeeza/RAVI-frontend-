from pydantic import BaseModel

class OCRResponse(BaseModel):
    text: str

class TTSResponse(BaseModel):
    audio_content: bytes  # base64-encoded in JSON, or streamed directly
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from app.schemas import OCRResponse
from app.services.ocr import OCRService
from app.services.tts import TTSService
from app.dependencies import get_ocr_service, get_tts_service
import io

app = FastAPI(title="Urdu OCR ↔ TTS")

@app.post("/ocr", response_model=OCRResponse)
async def ocr_endpoint(
    file: UploadFile = File(...),
    ocr: OCRService = Depends(get_ocr_service),
):
    img_bytes = await file.read()
    if not img_bytes:
        raise HTTPException(400, "Empty file")
    text = ocr.extract_text(img_bytes)
    return {"text": text}

@app.post("/tts")
async def tts_endpoint(
    payload: dict,
    tts: TTSService = Depends(get_tts_service),
):
    text = payload.get("text", "")
    if not text:
        raise HTTPException(400, "No text provided")
    audio = tts.synthesize(text)
    return StreamingResponse(io.BytesIO(audio), media_type="audio/mp3")

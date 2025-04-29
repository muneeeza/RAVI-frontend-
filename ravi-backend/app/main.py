from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.schemas import OCRResponse
from app.services.ocr import OCRService
from app.services.tts import TTSService
from app.dependencies import get_ocr_service, get_tts_service
import io

app = FastAPI(title="Ravi - Urdu Text Narrator")


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


@app.get("/health/gcp")
async def health_gcp(tts: TTSService = Depends(get_tts_service)):
    """
    Simple endpoint to verify that the Text-to-Speech client can authenticate
    and reach the GCP API.
    """
    try:
        # list_voices makes a lightweight API call
        voices = tts.client.list_voices().voices
        # return a small sample so you know it worked
        sample = [{"name": v.name, "language_codes": v.language_codes} for v in voices[:3]]
        return {"gcp_tts_ok": True, "sample_voices": sample}
    except Exception as e:
        # 503 Service Unavailable if auth or network fails
        raise HTTPException(503, detail=f"GCP TTS health-check failed: {e}")

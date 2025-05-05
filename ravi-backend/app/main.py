from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Body
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
    payload: dict = Body(...),
    tts: TTSService = Depends(get_tts_service),
):
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        audio = tts.synthesize(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")

    return StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")


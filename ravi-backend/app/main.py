from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import OCRResponse
from app.services.ocr import OCRService
from app.services.tts import TTSService
from app.dependencies import get_ocr_service, get_tts_service
import io

app = FastAPI(title="Urdu OCR → Text-to-Speech")

@app.post("/process", response_model=OCRResponse)
async def process_image(
    file: UploadFile = File(...),
    ocr: OCRService = Depends(get_ocr_service),
    tts: TTSService = Depends(get_tts_service),
):
    # 1. Read image bytes
    img_bytes = await file.read()
    if not img_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # 2. OCR → text
    extracted_text = ocr.extract_text(img_bytes)

    # 3. TTS → audio bytes
    audio_bytes = tts.synthesize(extracted_text)

    # 4. Return JSON and audio separately? Two approaches:

    # Option A: Return JSON with base64-encoded audio (works but larger payload)
    # return {"text": extracted_text, "audio_content": base64.b64encode(audio_bytes)}

    # Option B: Return text in JSON, and provide a separate endpoint to stream audio:
    # Here we demonstrate streaming audio directly:
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg"
    )

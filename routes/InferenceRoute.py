from services.AudioTokenizerService import get_audio_tokenizer_service
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import File, UploadFile
from models.audio import AudioFormat, FORMAT_BACKENDS, AudioRequest
from utils.utils import decode_base64_to_audio
import base64

audio_inference_router = APIRouter(
    prefix="/inference", tags=["audio"])


@audio_inference_router.post("")
async def tokenize_audio(request: AudioRequest):
    file_obj = decode_base64_to_audio(request.data)
    return get_audio_tokenizer_service().tokenize(file_obj, request.format)

from services.audio.AudioTokenizerService import get_audio_tokenizer_service
from fastapi import APIRouter
from services.audio.audio import AudioRequest
from common.converter_utility import decode_base64

audio_inference_router = APIRouter(
    prefix="/inference", tags=["audio"])


@audio_inference_router.post("")
async def tokenize_audio(request: AudioRequest):
    file_obj = decode_base64(request.data)
    return get_audio_tokenizer_service().tokenize(file_obj, request.format)

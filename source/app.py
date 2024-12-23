import argparse
import os
import sys
import time
import psutil
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, Path
from common.logger_utility import LoggerUtility
from services.audio.AudioTokenizerService import get_audio_tokenizer_service
from routes.AudioTokenizerRoute import audio_tokenizer_router
import uvicorn

from dotenv import load_dotenv


def parse_arguments():
    parser = argparse.ArgumentParser(description="WhisperVQ Application")
    parser.add_argument('--log-path', type=str, default='whisper.log', help='The log file path')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'TRACE'], help='The log level')
    parser.add_argument('--port', type=int, default=3348, help='The port to run the WhisperVQ app on')
    parser.add_argument('--device-id', type=str, default="0", help='The device ID to use')
    parser.add_argument('--package-dir', type=str, default="", help='The package directory to extend to sys.path')
    return parser.parse_args()


def configure_environment(args):
    sys.path.insert(0, args.package_dir)
    os.environ["CUDA_VISIBLE_DEVICES"] = args.device_id  # Use the specified Nvidia GPU


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_audio_tokenizer_service()
    yield


def create_app() -> FastAPI:

    app = FastAPI(lifespan=lifespan)
    app.include_router(audio_tokenizer_router)

    @app.delete("/destroy")
    async def destroy():
        threading.Thread(target=self_terminate, daemon=True).start()
        return {"success": True}

    return app


def self_terminate():
    time.sleep(1)
    parent = psutil.Process(psutil.Process(os.getpid()).ppid())
    parent.kill()


def main():
    env_path = Path(".variables") / ".env"
    load_dotenv(dotenv_path=env_path)
    args = parse_arguments()
    configure_environment(args)
    logger = LoggerUtility.configure_logging(args.log_path, args.log_level)

    LoggerUtility.configure_uvicorn_logging(args.log_path, args.log_level)

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()

from enum import Enum
from uvicorn.config import LOGGING_CONFIG
import logging


class LogLevelEnum(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    TRACE = "TRACE"


class LoggerUtility:

    @staticmethod
    def configure_uvicorn_logging(log_path: str, log_level: LogLevelEnum):
        LOGGING_CONFIG["handlers"]["default"] = {
            "class": "logging.FileHandler",
            "filename": log_path,
            "formatter": "default"
        }
        LOGGING_CONFIG["handlers"]["access"] = {
            "class": "logging.FileHandler",
            "filename": log_path,
            "formatter": "access"
        }
        LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] = log_level
        LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] = log_level

    @staticmethod
    def configure_logging(log_path: str, log_level: LogLevelEnum):
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path),
                # Uncomment the next line to enable console logging
                # logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        return logger

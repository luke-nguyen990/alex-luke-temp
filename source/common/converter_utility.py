import base64
import binascii


class ConverterUtility:

    @staticmethod
    def decode_base64(base64_string: str) -> bytes:
        try:
            bytes = base64.b64decode(base64_string)
            return bytes
        except binascii.Error as e:
            raise ValueError(f"Invalid base64 string: {e}")
        except IOError as e:
            raise IOError(f"Error: {e}")

    @staticmethod
    def encode_base64(byte_data: bytes) -> str:
        try:
            base64_encoded = base64.b64encode(byte_data).decode('utf-8')
            return base64_encoded
        except IOError as e:
            raise IOError(f"Error: {e}")

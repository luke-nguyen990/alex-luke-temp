### 1 Code structure

Suggested code-structure - Modular Monolith as follows:

```
source (src)
├── app.py
├── utility
│   ├── converter_utility.py
│   ├── generator_utility.py
│   └── logger_utility.py
├── services
    ├── audio
    │   ├── audio_controller.py
    │   ├── audio_interface.py
    │   ├── audio_model.py
    │   └── implementation
    │       └── audio_service.py
    ├── model
        ├── model_controller.py
        ├── model_interface.py
        ├── model_model.py
        └── implementation
            └── model_service.py
```

Contracts are exposed at the top level and implementation logic is hidden in the deeper folders.

### 2 All logics should be wrapped in a method, except for 1-2 exceptions in main.py
```
...
parser = argparse.ArgumentParser(description="WhisperVQ Application")
parser.add_argument('--log-path', type=str,
                    default='whisper.log', help='The log file path')
parser.add_argument('--log-level', type=str, default='INFO',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'TRACE'], help='The log level')
parser.add_argument('--port', type=int, default=3348,
                    help='The port to run the WhisperVQ app on')
parser.add_argument('--device-id', type=str, default="0",
                    help='The port to run the WhisperVQ app on')
parser.add_argument('--package-dir', type=str, default="",
                    help='The package-dir to be extended to sys.path')
args = parser.parse_args()
...
```
into
```
...
def parse_arguments():
    parser = argparse.ArgumentParser(description="WhisperVQ Application")
    parser.add_argument('--log-path', type=str, default='whisper.log', help='The log file path')
    parser.add_argument('--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'TRACE'], help='The log level')
    parser.add_argument('--port', type=int, default=3348, help='The port to run the WhisperVQ app on')
    parser.add_argument('--device-id', type=str, default="0", help='The device ID to use')
    parser.add_argument('--package-dir', type=str, default="", help='The package directory to extend to sys.path')
    return parser.parse_args()
...    
```

https://huggingface.co/cortexso/whispervq/blob/60bbff196e887bad2b8f2495c14ffa37f55fdfaa/download_model.py#L44

### 3 All methods should belong to a class (method is a verb, a verb must represent the action of sth)
for example
```
...
import urllib
from tqdm import tqdm
from huggingface_hub import hf_hub_download
import os

encoder_url = "https://huggingface.co/jan-hq/WhisperVQ/resolve/main/medium_encoder_only.pt"


def _download(url: str, root: str, in_memory: bool):
    os.makedirs(root, exist_ok=True)

    expected_sha256 = url.split("/")[-2]
    download_target = os.path.join(root, os.path.basename(url))

    if os.path.exists(download_target) and not os.path.isfile(download_target):
        raise RuntimeError
...
```
into

```
...
class ModelService:

    def __init__(self):
        self.download()

    def _download(url: str, root: str, in_memory: bool):
...    
```

### 4 __init__() is a constructor, it should not contain logic code

For example, please breaking the following constructor
```
...
class AudioTokenizerService:
    def __init__(self):
        self.available_backends = torchaudio.list_audio_backends()
        logger.info(f"Available backends: {self.available_backends}")
        main_directory = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)))

        # Verify ffmpeg support
        self.has_ffmpeg = "ffmpeg" in self.available_backends
        if not self.has_ffmpeg:
            logger.warning(
                "FFMPEG backend not available. Some formats may not be supported")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if not os.path.exists(main_directory+"/whisper-vq-stoks-v3-7lang-fixed.model"):
            hf_hub_download(
                repo_id="jan-hq/WhisperVQ",
                filename="whisper-vq-stoks-v3-7lang-fixed.model",
                local_dir=main_directory,
            )
        self.vq_model = CustomRQBottleneckTransformer.load_vq_only(
            main_directory +
            "/whisper-vq-stoks-v3-7lang-fixed.model"
        ).to(device)
        self.vq_model.load_encoder(device)
        self.vq_model.eval()
...
```

into sth like:
```
class AudioTokenizerService:
    def __init__(self):
        self._download_at_the_begin()


    def _download_at_the_begin():
        # TODO
```

### 5. Use singleton pattern for object which must be initiated one time only

### 6. String with limited options should be created as enum

### 7. Hardcoded/magic variables should be separated for configurable

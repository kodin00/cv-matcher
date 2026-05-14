import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent
BACKEND_ROOT = BACKEND_DIR.parent
DEFAULT_BASE_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_LOCAL_MODEL = "models/finetuned"


def _default_model_name() -> str:
    if (Path.cwd() / DEFAULT_LOCAL_MODEL).exists():
        return DEFAULT_LOCAL_MODEL
    if (BACKEND_ROOT / DEFAULT_LOCAL_MODEL).exists():
        return DEFAULT_LOCAL_MODEL
    return DEFAULT_BASE_MODEL


def _resolve_model_name(model_name: str) -> str:
    model_path = Path(model_name)

    if model_path.is_absolute() or (Path.cwd() / model_path).exists():
        return model_name

    backend_root_path = BACKEND_ROOT / model_path
    if backend_root_path.exists():
        return str(backend_root_path)

    return model_name


APP_TOKEN = os.getenv("APP_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
MODEL_NAME = _resolve_model_name(os.getenv("MODEL_NAME", _default_model_name()))

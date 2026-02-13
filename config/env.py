import os
from pathlib import Path
from dotenv import load_dotenv

_env_loaded = False


def load_env() -> None:
    global _env_loaded

    if _env_loaded:
        return

    env_path = Path(__file__).parent.parent / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

    _env_loaded = True


def get_env(key: str, default: str | None = None) -> str | None:
    """환경 변수 값을 가져온다."""
    return os.getenv(key, default)


def get_kakao_client_id() -> str | None:
    """Kakao Client ID를 가져온다."""
    return get_env("KAKAO_CLIENT_ID")


def get_kakao_redirect_uri() -> str | None:
    """Kakao Redirect URI를 가져온다."""
    return get_env("KAKAO_REDIRECT_URI")

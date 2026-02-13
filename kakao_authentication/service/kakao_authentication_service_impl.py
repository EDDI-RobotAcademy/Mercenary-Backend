from urllib.parse import urlencode

from config.settings import settings
from kakao_authentication.service.kakao_authentication_service import KakaoAuthenticationService


class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):
    __instance = None

    AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def generate_oauth_url(self) -> str:
        params = {
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type": "code",
        }

        return f"{self.AUTH_BASE_URL}?{urlencode(params)}"

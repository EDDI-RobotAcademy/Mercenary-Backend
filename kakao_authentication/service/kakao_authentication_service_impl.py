from urllib.parse import urlencode
from config.settings import get_settings
from kakao_authentication.repository.kakao_authentication_repository_impl import KakaoAuthenticationRepositoryImpl
from kakao_authentication.service.kakao_authentication_service import (
    KakaoAuthenticationService,
)
from kakao_authentication.service.response.kakao_token_response import KakaoTokenResponse


class KakaoAuthenticationServiceImpl(KakaoAuthenticationService):

    __instance = None
    AUTH_BASE_URL = "https://kauth.kakao.com/oauth/authorize"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.kakao_authentication_repository = (
                KakaoAuthenticationRepositoryImpl.getInstance()
            )

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def generate_oauth_url(self) -> str:
        settings = get_settings()

        params = {
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type": "code",
        }

        return f"{self.AUTH_BASE_URL}?{urlencode(params)}"

    def request_access_token(self, code: str) -> KakaoTokenResponse:
        if not code:
            raise ValueError("인가 코드가 필요합니다.")

        token_data = self.kakao_authentication_repository.request_access_token(code)

        return KakaoTokenResponse(**token_data)

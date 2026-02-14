import httpx
from fastapi import HTTPException
from config.settings import get_settings
from kakao_authentication.repository.kakao_authentication_repository import KakaoAuthenticationRepository


class KakaoAuthenticationRepositoryImpl(KakaoAuthenticationRepository):
    __instance = None
    TOKEN_URL = "https://kauth.kakao.com/oauth/token"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def request_access_token(self, code: str) -> dict:
        settings = get_settings()

        payload = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        }

        try:
            response = httpx.post(
                self.TOKEN_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10.0
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Kakao 서버 요청 실패")

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Kakao 토큰 요청 실패: {response.text}"
            )

        return response.json()

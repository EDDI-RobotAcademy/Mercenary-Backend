from fastapi import APIRouter, Depends

from kakao_authentication.service.kakao_authentication_service_impl import KakaoAuthenticationServiceImpl

kakao_authentication_router = APIRouter(prefix="/kakao-authentication")

def inject_kakao_authentication_service() -> KakaoAuthenticationServiceImpl:
    return KakaoAuthenticationServiceImpl.getInstance()

@kakao_authentication_router.get("/request-oauth-link")
def request_oauth_link(
    kakao_service: KakaoAuthenticationServiceImpl =
    Depends(inject_kakao_authentication_service)
):
    oauth_url = kakao_service.generate_oauth_url()

    return {
        "kakao_oauth_url": oauth_url
    }

from fastapi import APIRouter, Depends, Query, HTTPException

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

@kakao_authentication_router.get("/request-access-token-after-redirection")
def request_access_token_after_redirection(
    code: str = Query(...),
    kakao_service: KakaoAuthenticationServiceImpl =
    Depends(inject_kakao_authentication_service)
):
    try:
        return kakao_service.login_with_kakao(code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

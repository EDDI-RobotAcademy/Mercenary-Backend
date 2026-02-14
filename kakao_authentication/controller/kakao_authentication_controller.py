from fastapi import APIRouter, Depends, Query, HTTPException, Response

from authentication.service.authentication_service_impl import AuthenticationServiceImpl
from kakao_authentication.service.kakao_authentication_service_impl import KakaoAuthenticationServiceImpl

kakao_authentication_router = APIRouter(prefix="/kakao-authentication")

def inject_kakao_authentication_service() -> KakaoAuthenticationServiceImpl:
    return KakaoAuthenticationServiceImpl.getInstance()

def inject_authentication_service() -> AuthenticationServiceImpl:
    return AuthenticationServiceImpl.get_instance()

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
    response: Response,
    code: str = Query(...),
    kakao_service: KakaoAuthenticationServiceImpl =
    Depends(inject_kakao_authentication_service),
    auth_service: AuthenticationServiceImpl =
    Depends(inject_authentication_service)
):
    try:
        login_response = kakao_service.login_with_kakao(code)

        # 🔐 세션 생성
        user_token = auth_service.create_session(login_response.user_id)

        # 🍪 Cookie 발급
        response.set_cookie(
            key="userToken",
            value=user_token,
            httponly=True,
            secure=True,        # HTTPS 환경 필수
            samesite="lax",
            max_age=3600        # 1시간
        )

        return login_response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, Query, HTTPException, Response

from account.domain.value_objects.login_type import LoginType
from account_profile.domain.value_objects.email import Email
from account_profile.domain.value_objects.nickname import Nickname
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from authentication.service.authentication_service_impl import AuthenticationServiceImpl
from kakao_authentication.service.kakao_authentication_service_impl import KakaoAuthenticationServiceImpl

kakao_authentication_router = APIRouter(prefix="/kakao-authentication")

def inject_kakao_authentication_service() -> KakaoAuthenticationServiceImpl:
    return KakaoAuthenticationServiceImpl.getInstance()

def inject_authentication_service() -> AuthenticationServiceImpl:
    return AuthenticationServiceImpl.get_instance()

def inject_account_profile_service() -> AccountProfileServiceImpl:
    return AccountProfileServiceImpl.get_instance()

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
    kakao_service: KakaoAuthenticationServiceImpl = Depends(inject_kakao_authentication_service),
    auth_service: AuthenticationServiceImpl = Depends(inject_authentication_service),
    account_profile_service: AccountProfileServiceImpl = Depends(inject_account_profile_service)
):
    try:
        # Kakao API로 로그인 & 사용자 정보 조회
        kakao_user_info = kakao_service.login_with_kakao(code)
        email = Email(kakao_user_info.email)
        nickname = Nickname(kakao_user_info.nickname)

        # AccountProfile 조회: 기존 회원인지 확인
        profile = account_profile_service.find_by_email_and_login_type(
            email=email,
            login_type=LoginType.KAKAO.value
        )

        if profile is None:
            temp_token = auth_service.create_temp_session(kakao_user_info.access_token)
            response.set_cookie(
                key="tempToken",
                value=temp_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=int(AuthenticationServiceImpl.TEMP_SESSION_TTL.total_seconds())
            )

            return {
                "temp_token": temp_token,
                "nickname": nickname.value,
                "email": email.value,
                "login_type": LoginType.KAKAO.value,
                "is_temp_user": True
            }

        # 인증 세션 (Redis)
        user_token = auth_service.create_session(profile.account.id, kakao_user_info.access_token)

        response.set_cookie(
            key="userToken",
            value=user_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600
        )

        return {
            "nickname": nickname.value,
            "email": email.value,
            "login_type": LoginType.KAKAO.value,
            "is_temp_user": False
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

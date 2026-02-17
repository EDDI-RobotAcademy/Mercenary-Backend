from fastapi import APIRouter, Depends, Cookie, HTTPException

from authentication.service.authentication_service_impl import AuthenticationServiceImpl
from account.service.account_service_impl import AccountServiceImpl
from kakao_authentication.service.kakao_authentication_service_impl import (
    KakaoAuthenticationServiceImpl,
)

authentication_router = APIRouter(prefix="/authentication")


def inject_auth_service() -> AuthenticationServiceImpl:
    return AuthenticationServiceImpl.get_instance()


def inject_account_service() -> AccountServiceImpl:
    return AccountServiceImpl.get_instance()


def inject_kakao_service() -> KakaoAuthenticationServiceImpl:
    return KakaoAuthenticationServiceImpl.getInstance()


@authentication_router.get("/status")
def get_authentication_status(
    userToken: str | None = Cookie(default=None),
    tempToken: str | None = Cookie(default=None),
    auth_service: AuthenticationServiceImpl = Depends(inject_auth_service),
    account_service: AccountServiceImpl = Depends(inject_account_service),
    kakao_service: KakaoAuthenticationServiceImpl = Depends(inject_kakao_service),
):
    # 정회원 세션 확인
    if userToken:
        account_id = auth_service.validate_session(userToken)

        if not account_id:
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        account = account_service.lookup(account_id)

        if not account:
            raise HTTPException(status_code=401, detail="Account not found")

        return {
            "nickname": account.profile.nickname.value,
            "email": account.profile.email.value,
            "login_type": account.login_type.value,
            "is_temp_user": False,
        }

    # 임시 세션 확인
    if tempToken:
        kakao_access_token = auth_service.get_temp_session(tempToken)

        if not kakao_access_token:
            raise HTTPException(status_code=401, detail="Invalid or expired temp session")

        # Kakao API 통해 사용자 정보 조회
        account = kakao_service.get_user_info(kakao_access_token)

        return {
            "nickname": account.profile.nickname.value,
            "email": account.profile.email.value,
            "login_type": account.login_type.value,
            "is_temp_user": True,
        }

    # 쿠키 없음
    raise HTTPException(status_code=401, detail="Not authenticated")

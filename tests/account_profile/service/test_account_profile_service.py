import pytest
from unittest.mock import MagicMock

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from account_profile.domain.value_objects.email import Email
from account_profile.domain.value_objects.nickname import Nickname
from account.domain.value_objects.login_type import LoginType

# ----------------------------
# Mock Repository Fixture
# ----------------------------
@pytest.fixture
def mock_repository():
    mock_repo = MagicMock()
    return mock_repo

# ----------------------------
# Service Fixture
# ----------------------------
@pytest.fixture
def account_profile_service(mock_repository):
    service = AccountProfileServiceImpl.get_instance()
    # private repository 주입
    service._AccountProfileServiceImpl__account_profile_repository = mock_repository
    return service

# ----------------------------
# 테스트 케이스
# ----------------------------
def test_find_existing_account_profile(account_profile_service, mock_repository):
    email = Email("test@example.com")
    nickname = Nickname("Tester")

    # AccountProfile mock 객체 생성
    mock_profile = MagicMock()
    mock_profile.email.value = email.value
    mock_profile.nickname.value = nickname.value
    mock_profile.login_type = LoginType.KAKAO

    # repository 호출 시 mock 반환
    mock_repository.find_with_account_by_email_and_login_type.return_value = mock_profile

    # 서비스 호출
    found_profile = account_profile_service.find_by_email_and_login_type(
        email=email,
        login_type=LoginType.KAKAO
    )

    # 검증
    assert found_profile is not None
    assert found_profile.email.value == "test@example.com"
    assert found_profile.nickname.value == "Tester"
    assert found_profile.login_type == LoginType.KAKAO

def test_find_nonexistent_account_profile(account_profile_service, mock_repository):
    email = Email("notexist@example.com")

    # repository가 None 반환
    mock_repository.find_with_account_by_email_and_login_type.return_value = None

    profile = account_profile_service.find_by_email_and_login_type(
        email=email,
        login_type=LoginType.KAKAO
    )

    assert profile is None

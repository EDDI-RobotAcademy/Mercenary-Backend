from typing import Optional
from account_profile.domain.entity.account_profile import AccountProfile
from account_profile.domain.value_objects.email import Email
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from account_profile.service.account_profile_service import AccountProfileService
from account.domain.value_objects.login_type import LoginType

class AccountProfileServiceImpl(AccountProfileService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__account_profile_repository = AccountProfileRepositoryImpl.get_instance()
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_by_email_and_login_type(self, email: Email, login_type: LoginType) -> Optional[AccountProfile]:
        return self.__account_profile_repository.find_with_account_by_email_and_login_type(
            email.value, login_type
        )

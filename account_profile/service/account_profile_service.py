from abc import ABC, abstractmethod
from typing import Optional

from account.domain.value_objects.login_type import LoginType
from account_profile.domain.entity.account_profile import AccountProfile
from account_profile.domain.value_objects.email import Email


class AccountProfileService(ABC):

    @abstractmethod
    def find_by_email_and_login_type(
            self, email: Email, login_type: LoginType
    ) -> Optional[AccountProfile]:
        pass

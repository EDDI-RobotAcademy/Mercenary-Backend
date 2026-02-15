from abc import ABC, abstractmethod
from typing import Optional

from account.domain.value_objects.login_type import LoginType
from account_profile.domain.entity.account_profile import AccountProfile


class AccountProfileRepository(ABC):

    @abstractmethod
    def find_with_account_by_email_and_login_type(
        self, email: str, login_type: LoginType
    ) -> Optional[AccountProfile]:
        pass

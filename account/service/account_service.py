from abc import ABC, abstractmethod

from account.domain.entity.account import Account
from account.domain.value_objects.email import Email
from account.domain.value_objects.nickname import Nickname


class AccountService(ABC):

    @abstractmethod
    def register(
            self,
            login_type: str,
            email: Email,
            nickname: Nickname
    ) -> Account:
        pass

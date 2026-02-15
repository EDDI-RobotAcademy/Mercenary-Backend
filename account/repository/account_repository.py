from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from account.domain.entity.account import Account


class AccountRepository(ABC):

    @abstractmethod
    def save(self, session: Session, account: Account) -> Account:
        pass

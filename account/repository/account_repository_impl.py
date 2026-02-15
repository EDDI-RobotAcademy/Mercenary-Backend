from account.domain.entity.account import Account
from account.repository.account_repository import AccountRepository
from sqlalchemy.orm import Session

class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def save(self, session: Session, account: Account) -> Account:
        session.add(account)
        return account

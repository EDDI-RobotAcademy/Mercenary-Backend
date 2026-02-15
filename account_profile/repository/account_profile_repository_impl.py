from typing import Optional
import logging
from sqlalchemy.orm import Session, joinedload

from account.domain.value_objects.login_type import LoginType
from account_profile.domain.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository import AccountProfileRepository
from config.mysql_config import MySQLConfig

logger = logging.getLogger(__name__)

class AccountProfileRepositoryImpl(AccountProfileRepository):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _initialize(self):
        self._session: Session = MySQLConfig().get_session()

    def find_with_account_by_email_and_login_type(
        self, email: str, login_type: LoginType
    ) -> Optional[AccountProfile]:
        try:
            profile = (
                self._session.query(AccountProfile)
                .options(joinedload(AccountProfile.account))
                .filter(
                    AccountProfile.email == email,
                    AccountProfile.login_type == login_type.value
                )
                .one_or_none()
            )
            return profile
        except Exception as e:
            logger.error(f"DB 조회 실패: {e}")
            return None

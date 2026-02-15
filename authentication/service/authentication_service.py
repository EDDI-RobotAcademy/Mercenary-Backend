from abc import ABC, abstractmethod


class AuthenticationService(ABC):

    @abstractmethod
    def create_session(self, account_id: str, kakao_access_token: str) -> str:
        pass

    @abstractmethod
    def create_temp_session(self, kakao_access_token: str) -> str:
        pass

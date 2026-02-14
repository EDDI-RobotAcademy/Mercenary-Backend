from abc import ABC, abstractmethod


class AuthenticationService(ABC):

    @abstractmethod
    def create_session(self, user_id: int) -> str:
        pass
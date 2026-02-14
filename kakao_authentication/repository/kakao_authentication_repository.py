from abc import ABC, abstractmethod


class KakaoAuthenticationRepository(ABC):

    @abstractmethod
    def request_access_token(self, code: str) -> dict:
        pass
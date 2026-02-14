from abc import ABC, abstractmethod

from kakao_authentication.service.response.kakao_token_response import KakaoTokenResponse


class KakaoAuthenticationService(ABC):

    @abstractmethod
    def generate_oauth_url(self) -> str:
        pass

    @abstractmethod
    def request_access_token(self, code: str) -> KakaoTokenResponse:
        pass


from abc import ABC, abstractmethod

class KakaoAuthenticationService(ABC):

    @abstractmethod
    def generate_oauth_url(self) -> str:
        pass
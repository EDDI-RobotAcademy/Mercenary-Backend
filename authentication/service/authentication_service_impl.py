from datetime import timedelta
import uuid

from redis_cache.repository.redis_cache_repository_impl import RedisCacheRepositoryImpl


class AuthenticationServiceImpl:
    _instance = None
    SESSION_TTL = timedelta(hours=1)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.redis = RedisCacheRepositoryImpl.get_instance()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_session(self, user_id: str) -> str:
        # 유니크한 토큰 생성
        user_token = str(uuid.uuid4())

        # Redis에 저장
        self.redis.set_key_and_value(
            key=f"session:{user_token}",
            value=user_id,
            ttl=self.SESSION_TTL
        )

        return user_token

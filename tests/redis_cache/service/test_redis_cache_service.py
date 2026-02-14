import time
from datetime import timedelta

import pytest

from redis_cache.repository.redis_cache_repository_impl import RedisCacheRepositoryImpl


@pytest.fixture(scope="module")
def redis_service():
    service = RedisCacheRepositoryImpl.get_instance()
    yield service
    # 테스트 종료 후 정리
    service.redis_client.flushdb()


def test_set_and_get(redis_service):
    redis_service.set_key_and_value("test:key", "value1")

    result = redis_service.get_value_by_key("test:key", str)

    assert result == "value1"


def test_delete(redis_service):
    redis_service.set_key_and_value("delete:key", "value2")

    redis_service.delete_by_key("delete:key")

    result = redis_service.get_value_by_key("delete:key", str)

    assert result is None


def test_ttl_expiration(redis_service):
    redis_service.set_key_and_value(
        "ttl:key",
        "temp",
        ttl=timedelta(seconds=2)
    )

    time.sleep(3)

    result = redis_service.get_value_by_key("ttl:key", str)

    assert result is None


def test_refresh_token_exists(redis_service):
    token = "refresh:token:123"

    redis_service.set_key_and_value(token, "user1")

    assert redis_service.is_refresh_token_exists(token) is True

    redis_service.delete_by_key(token)

    assert redis_service.is_refresh_token_exists(token) is False

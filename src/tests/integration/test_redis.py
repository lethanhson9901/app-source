# app-source/src/tests/integration/test_redis.py
import pytest
import aioredis
from ...app.config import settings

@pytest.mark.asyncio
async def test_redis_operations():
    redis = aioredis.from_url(settings.REDIS_URL)
    
    try:
        # Test Set and Get
        await redis.set("test_key", "test_value")
        value = await redis.get("test_key")
        assert value.decode() == "test_value"
        
        # Test Expiry
        await redis.set("expire_key", "expire_value", ex=1)
        assert await redis.get("expire_key") is not None
        await asyncio.sleep(1.1)
        assert await redis.get("expire_key") is None
        
        # Test List Operations
        await redis.lpush("test_list", "item1", "item2", "item3")
        assert await redis.llen("test_list") == 3
        assert await redis.lpop("test_list") == b"item3"
        
        # Test Hash Operations
        await redis.hset(
            "test_hash",
            mapping={"field1": "value1", "field2": "value2"}
        )
        assert await redis.hget("test_hash", "field1") == b"value1"
        assert await redis.hgetall("test_hash") == {
            b"field1": b"value1",
            b"field2": b"value2"
        }
        
    finally:
        await redis.delete("test_key")
        await redis.delete("test_list")
        await redis.delete("test_hash")
        await redis.close()
import json
from redis_client import redis_client

CACHE_TTL_SECONDS = 60


def get_cache(key):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print("Cache Get Error:", e)
    return None


def set_cache(key, value, ttl=CACHE_TTL_SECONDS):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        print("Cache Set Error:", e)


def clear_cache_prefix(prefix):
    try:
        for key in redis_client.scan_iter(f"{prefix}*"):
            redis_client.delete(key)
    except Exception as e:
        print("Cache Clear Error:", e)
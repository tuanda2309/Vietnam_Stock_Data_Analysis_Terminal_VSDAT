import copy
import threading
import time


_CACHE = {}
_LOCK = threading.Lock()


def cache_get(key):
    now = time.time()
    with _LOCK:
        item = _CACHE.get(key)
        if not item:
            return None
        expires_at, value = item
        if expires_at <= now:
            _CACHE.pop(key, None)
            return None
        return copy.deepcopy(value)


def cache_set(key, value, ttl_seconds):
    if ttl_seconds <= 0:
        return
    with _LOCK:
        _CACHE[key] = (time.time() + ttl_seconds, copy.deepcopy(value))


def cache_clear_expired():
    now = time.time()
    with _LOCK:
        expired_keys = [key for key, (expires_at, _) in _CACHE.items() if expires_at <= now]
        for key in expired_keys:
            _CACHE.pop(key, None)

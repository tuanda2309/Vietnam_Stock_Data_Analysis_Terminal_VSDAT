import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        os.environ.get("RATELIMIT_DEFAULT", "120 per minute"),
        os.environ.get("RATELIMIT_DAILY", "1000 per day"),
    ],
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"),
)

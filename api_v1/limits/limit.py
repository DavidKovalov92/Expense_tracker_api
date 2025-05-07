import redis
from datetime import timedelta


r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


USER_RATE_LIMIT_KEY = "10:{user_id}"
SERVICE_RATE_LIMIT_KEY = "5000"
RATE_LIMIT = 5
WINDOW = 60

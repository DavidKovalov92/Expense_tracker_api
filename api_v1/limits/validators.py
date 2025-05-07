import time
from fastapi import Request

from fastapi import HTTPException
from .limit import RATE_LIMIT, WINDOW, r

from api_v1.limits.limit import SERVICE_RATE_LIMIT_KEY, USER_RATE_LIMIT_KEY

def is_rate_limited(user_id: int):
    # Ключ для ліміту користувача
    user_key = USER_RATE_LIMIT_KEY.format(user_id=user_id)
    
    # Ліміт на 10 запитів за 60 секунд для кожного користувача
    user_limit = 10
    user_time_window = 60
    
    # Перевіряємо лічильник запитів для конкретного користувача
    user_requests = r.get(user_key)
    if user_requests and int(user_requests) >= user_limit: # type: ignore
        raise HTTPException(status_code=429, detail="User rate limit exceeded")
    
    # Якщо лічильник не існує або він менший ліміту, збільшуємо його
    pipe = r.pipeline()
    pipe.incr(user_key)
    pipe.expire(user_key, user_time_window)  # Термін дії лічильника 60 секунд
    pipe.execute()

def is_global_rate_limited():
    # Ліміт на 5000 запитів за 60 секунд для всього сервісу
    global_limit = 5000
    global_time_window = 60
    
    # Перевіряємо глобальний лічильник запитів
    global_requests = r.get(SERVICE_RATE_LIMIT_KEY)
    if global_requests and int(global_requests) >= global_limit: # type: ignore
        raise HTTPException(status_code=429, detail="Global rate limit exceeded")
    
    # Якщо лічильник не існує або він менший ліміту, збільшуємо його
    pipe = r.pipeline()
    pipe.incr(SERVICE_RATE_LIMIT_KEY)
    pipe.expire(SERVICE_RATE_LIMIT_KEY, global_time_window)  # Термін дії лічильника 60 секунд
    pipe.execute()
    
    


ip_requests = {}

def rate_limit_ip(ip: str):
    import time
    now = time.time()
    requests = ip_requests.get(ip, [])
    requests = [r for r in requests if now - r < WINDOW]
    if len(requests) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many registration attempts from this IP")
    requests.append(now)
    ip_requests[ip] = requests


import asyncio
import httpx
from functools import wraps
def async_retry(retries=3, backoff=2, exceptions=(httpx.RequestError, httpx.HTTPStatusError)):
    """
    异步重试装饰器
    retries: 最大重试次数
    backoff: 指数退避基数
    exceptions: 捕获的异常类型元组
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    print(f"第 {attempt} 次请求失败: {e}")
                    if attempt == retries:
                        break
                    await asyncio.sleep(backoff ** attempt)
            return None
        return wrapper
    return decorator
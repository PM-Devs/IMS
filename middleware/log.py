# middleware/log.py
import time
from fastapi import Request

async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} - Process Time: {process_time:.4f}s")
    return response

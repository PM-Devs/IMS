
# middleware/requestValidity.py
from fastapi import Request, HTTPException
import re

async def request_validity_middleware(request: Request, call_next):
    content_type = request.headers.get("Content-Type")
    if request.method in ["POST", "PUT", "PATCH"] and not content_type:
        raise HTTPException(status_code=400, detail="Content-Type header is required")
    
    if content_type and "application/json" in content_type:
        body = await request.body()
        if len(body) > 1_000_000:  # 1 MB limit
            raise HTTPException(status_code=413, detail="Request body too large")
    

    response = await call_next(request)
    return response
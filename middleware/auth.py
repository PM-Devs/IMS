from fastapi import Request, HTTPException
from services.service import verify_app_credentials, is_token_blacklisted

async def auth_middleware(request: Request, call_next):
    # List of paths that don't require authentication
    open_paths = ["/docs", "/openapi.json", "/redoc"]
    
    # Skip authentication checks for open paths
    if request.url.path in open_paths:
        return await call_next(request)

    # Retrieve application credentials from headers
    app_id = request.headers.get("X-App-ID")
    app_key = request.headers.get("X-App-Key")
    
    # Check if application credentials are missing
    if not app_id or not app_key:
        raise HTTPException(status_code=400, detail="Missing application credentials")
    
    # Verify application credentials
    if not await verify_app_credentials(app_id, app_key):
        raise HTTPException(status_code=401, detail="Invalid application credentials")
    
    # Check Authorization header for token
    authorization = request.headers.get("Authorization")
    if authorization:
        try:
            token_type, token = authorization.split()
            # Ensure token format is correct
            if token_type.lower() != "bearer" or not token:
                raise HTTPException(status_code=400, detail="Invalid Authorization header format")
            # Check if token is blacklisted
            if await is_token_blacklisted(token):
                raise HTTPException(status_code=401, detail="Token has been revoked")
        except (ValueError, IndexError):
            raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    # Proceed to the next middleware or endpoint
    response = await call_next(request)
    return response

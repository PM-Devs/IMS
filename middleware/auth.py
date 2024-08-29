from fastapi import Request, Response
from starlette.status import HTTP_401_UNAUTHORIZED
from services.service import verify_app_credentials, is_token_blacklisted

async def auth_middleware(request: Request, call_next):
    # List of paths that don't require authentication
    open_paths = ["/docs", "/openapi.json", "/"]
    
    # Skip authentication checks for open paths
    if request.url.path in open_paths:
        return await call_next(request)

    # Retrieve application credentials from headers
    app_id = request.headers.get("X-App-ID")
    app_key = request.headers.get("X-App-Key")
    
    # Check if application credentials are missing
    if not app_id or not app_key:
        return Response(content="Unauthorized: Missing application credentials", status_code=HTTP_401_UNAUTHORIZED)
    
    # Verify application credentials
    if not await verify_app_credentials(app_id, app_key):
        return Response(content="Unauthorized: Invalid application credentials", status_code=HTTP_401_UNAUTHORIZED)
    
    # Check Authorization header for token
    authorization = request.headers.get("Authorization")
    if authorization:
        try:
            token_type, token = authorization.split()
            # Ensure token format is correct
            if token_type.lower() != "bearer" or not token:
                return Response(content="Unauthorized: Invalid Authorization header format", status_code=HTTP_401_UNAUTHORIZED)
            # Check if token is blacklisted
            if await is_token_blacklisted(token):
                return Response(content="Unauthorized: Token has been revoked", status_code=HTTP_401_UNAUTHORIZED)
        except (ValueError, IndexError):
            return Response(content="Unauthorized: Invalid Authorization header format", status_code=HTTP_401_UNAUTHORIZED)

    # Proceed to the next middleware or endpoint
    response = await call_next(request)
    return response

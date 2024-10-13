
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "da748h&^&H7r7h7syhds76he7w6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = True
    if user is None:
        raise credentials_exception
    return user
check=get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyNEBleGFtcGxlLmNvbSIsImV4cCI6MTczMTQxODI5Mn0.VLxuClKI9YyAZ69gb6n27M5-6JtHLk3OWioW7SIKR0Q")
print(check)
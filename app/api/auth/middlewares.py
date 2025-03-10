import jwt
from dotenv import dotenv_values
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jwt.exceptions import PyJWTError


config = dotenv_values()
SECRET_KEY = config['SECRET_KEY']
ALGORITHM = config['ALGORITH']
PUBLICPATHS = ["/auth/login", "/users", "/docs", "/openapi.json"]


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Allows usage of public endpoints
        if any(request.url.path.startswith(path) for path in PUBLICPATHS):
            return await call_next(request)
        # get headers token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Token not found"})
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload.get("sub")  # save user in request
        except PyJWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid Token"})
        return await call_next(request)

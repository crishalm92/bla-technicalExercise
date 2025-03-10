from functools import wraps
from fastapi import HTTPException, Request


def requires_auth(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        if not hasattr(request.state, "user") or not request.state.user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return await func(*args, request=request, **kwargs)
    return wrapper

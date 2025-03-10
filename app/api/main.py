from fastapi import FastAPI
from app.api.users.users import router as users_router
from app.api.tasks.tasks import router as items_router
from app.api.auth.auth import router as auth_router
from app.api.auth.middlewares import JWTAuthMiddleware
from fastapi.openapi.utils import get_openapi


app = FastAPI()

app.add_middleware(JWTAuthMiddleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "auth/login",
                    "scopes": {},
                }
            }
        }
    }
    for route in app.routes:
        if hasattr(route.endpoint, "requires_auth") and route.endpoint.requires_auth:
            path = f"/{route.path.lstrip('/')}"
            if path in openapi_schema["paths"]:
                openapi_schema["paths"][path]["get"]["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(items_router)


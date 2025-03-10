from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .utils import create_access_token, verify_password
from app.repository.user_repository import UsersRepoImplementation


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
user_repository = UsersRepoImplementation()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_repository.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect user or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

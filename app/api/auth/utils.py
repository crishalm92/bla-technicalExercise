import jwt
from dotenv import dotenv_values
from datetime import timedelta, datetime
from passlib.context import CryptContext


config = dotenv_values()
SECRET_KEY = config['SECRET_KEY']
ALGORITH = config['ALGORITH']
ACCESS_TOKEN_EXPIRE_MINUTES = int(config['ACCESS_TOKEN_EXPIRE_MINUTES'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)

from jose import jwt
from datetime import timedelta, datetime, timezone
from app.settings import ALGORITHM, SECRET_KEY


def create_acces_token(sub: dict) -> str:
    to_encode = sub.copy()
    acccess_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return acccess_token


def create_refreh_token(sub: dict) -> str:
    to_encode = sub.copy()
    exprire_in = datetime.now(timezone.utc) + timedelta(days=3)
    to_encode.update({"exp": exprire_in})
    refreh_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return refreh_token


def decode_token(token: str) -> dict:
    token_data = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    return token_data

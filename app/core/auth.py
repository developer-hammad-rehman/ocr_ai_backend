from unittest import result
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_username(username:str , db_username:str) -> bool:
    return username == db_username


def verify_password(plain_password:str , hash_password:str) -> bool:
    return pwd_context.verify(plain_password , hash_password)

def get_hash_password(plain_password:str) -> str:
    return pwd_context.hash(plain_password)



def verify_creditials(username : str , password:str , session : Session) -> bool:
    statment = select(Users).where(username == Users.username)
    result = session.exec(statment).first()
    if result:
     is_email = verify_username(username=username , db_username=result.username)
     if is_email:
        is_password = verify_password(plain_password=password , hash_password=result.password)
        return is_password
     else:
        return is_email
    else:
       return False
    

def get_username(username:str , session:Session):
    statment = select(Users).where(username == Users.username)
    result = session.exec(statment).first()
    return True if result else False


from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.crud import get_session
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm

#=====================================================================================#

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth")

#=======================================================================================#

FORMDEP = Annotated[OAuth2PasswordRequestForm , Depends()]

#=========================================================================================#

OAUTHDEP = Annotated[str , Depends(oauth_scheme)]

#===========================================================================================#

DBSESSION = Annotated[Session, Depends(get_session)]

#===========================================================================================#
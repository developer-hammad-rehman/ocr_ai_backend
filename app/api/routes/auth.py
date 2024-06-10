from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException

from app.api.deps import DBSESSION, FORMDEP
from app.core.auth import get_hash_password, get_username, verify_creditials
from app.core.token import create_acces_token, create_refreh_token
from app.models import Token, Users

auth_router = APIRouter(tags=["Auth Routes"])

@auth_router.post("/auth")
async def auth_route(formdata: FORMDEP , session:DBSESSION):
    is_authenticate = verify_creditials(username=formdata.username , password=formdata.password , session=session)
    if is_authenticate:
        exprire_in = datetime.now(timezone.utc) + timedelta(hours=1)
        access_token = create_acces_token(sub={"username":formdata.username , "exp":exprire_in})
        refresh_token = create_refreh_token(sub={"username":formdata.username})
        return Token(access_token=access_token , refresh_token=refresh_token , expires_in=exprire_in)
    else:
        raise HTTPException(status_code=404 , detail="Email and Password are wrong" ,headers={"WWW-Authenticate": "Bearer"})
    

@auth_router.post("/register")
async def register_route(formdata:FORMDEP , session:DBSESSION):
    is_username = get_username(username=formdata.username , session=session)
    if not is_username:
        hash_password = get_hash_password(plain_password=formdata.password)
        data = Users(username=formdata.username , password=hash_password)
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    else:
        raise HTTPException(status_code=404 , detail="Username already usernaem")
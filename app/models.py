from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str


class FileUpload(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class Token:
    def __init__(self, access_token: str, expires_in: datetime, refresh_token: str):
        self.access_token = access_token
        self.token_type = "bearer"
        self.expires_in = expires_in
        self.refresh_token = refresh_token


class ReviewResult(SQLModel):
    discrepancies: dict
    missing_information: dict
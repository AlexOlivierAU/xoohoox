from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: str
    password: str
    full_name: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None

# Properties shared by models stored in DB
class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

# Additional properties stored in DB
class UserInDB(User):
    hashed_password: str 
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

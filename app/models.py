from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    birth_date: date = Field(..., description="Data de nascimento")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade onde reside")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v > date.today():
            raise ValueError('Data de nascimento não pode ser no futuro')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode estar vazio')
        return v.strip().title()
    
    @validator('city')
    def validate_city(cls, v):
        if not v.strip():
            raise ValueError('Cidade não pode estar vazia')
        return v.strip().title()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao@email.com",
                "birth_date": "1990-01-15",
                "city": "São Paulo"
            }
        }

class UserUpdateModel(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError('Data de nascimento não pode ser no futuro')
        return v

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    birth_date: str
    city: str
    created_at: str
    updated_at: Optional[str] = None
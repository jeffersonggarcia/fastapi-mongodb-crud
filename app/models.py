from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Annotated
from datetime import date, datetime
from bson import ObjectId


# Usamos Annotated para definir um tipo customizado para ObjectId
PyObjectId = Annotated[str, Field(description="MongoDB ObjectId")]


def validate_object_id(v: str) -> str:
    """Valida se uma string é um ObjectId válido"""
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return str(v)


class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", description="MongoDB ObjectId")
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    birth_date: date = Field(..., description="Data de nascimento")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade onde reside")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        if v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode estar vazio")
        return v.strip().title()

    @field_validator("city")
    @classmethod
    def validate_city(cls, v):
        if not v.strip():
            raise ValueError("Cidade não pode estar vazia")
        return v.strip().title()

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "name": "João Silva",
                "email": "joao@email.com",
                "birth_date": "1990-01-15",
                "city": "São Paulo"
            }
        }
    }


class UserUpdateModel(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro")
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    birth_date: str
    city: str
    created_at: str
    updated_at: Optional[str] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }


# Helper para converter o documento Mongo para dict compatível com UserResponse
def user_helper(user_doc: dict) -> dict:
    return {
        "id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "email": user_doc["email"],
        "birth_date": user_doc["birth_date"].isoformat() if isinstance(user_doc["birth_date"], (date, datetime)) else user_doc["birth_date"],
        "city": user_doc["city"],
        "created_at": user_doc["created_at"].isoformat() if isinstance(user_doc.get("created_at"), (date, datetime)) else user_doc.get("created_at"),
        "updated_at": user_doc.get("updated_at").isoformat() if user_doc.get("updated_at") and isinstance(user_doc.get("updated_at"), (date, datetime)) else user_doc.get("updated_at"),
    }
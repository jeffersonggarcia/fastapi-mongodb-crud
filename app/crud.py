from .database import db
from .schemas import user_helper
from .models import UserModel, UserUpdateModel
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

collection = db["users"]

async def create_user(user: UserModel):
    # Verificar se email já existe
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já está em uso")
    
    user_data = user.dict(by_alias=True, exclude_unset=True)
    user_data["created_at"] = datetime.utcnow()
    
    res = await collection.insert_one(user_data)
    created_user = await collection.find_one({"_id": res.inserted_id})
    return user_helper(created_user)

async def get_users(skip: int = 0, limit: int = 100):
    users = []
    cursor = collection.find().skip(skip).limit(limit)
    async for user in cursor:
        users.append(user_helper(user))
    return users

async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user_helper(user)

async def update_user(user_id: str, user_update: UserUpdateModel):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    # Verificar se usuário existe
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se novo email já está em uso por outro usuário
    if user_update.email:
        email_exists = await collection.find_one({
            "email": user_update.email,
            "_id": {"$ne": ObjectId(user_id)}
        })
        if email_exists:
            raise HTTPException(status_code=400, detail="Email já está em uso")
    
    update_data = user_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    res = await collection.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"message": "Usuário deletado com sucesso"}

async def search_users(query: str, skip: int = 0, limit: int = 100):
    """Buscar usuários por nome, email ou cidade"""
    search_filter = {
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}},
            {"city": {"$regex": query, "$options": "i"}}
        ]
    }
    
    users = []
    cursor = collection.find(search_filter).skip(skip).limit(limit)
    async for user in cursor:
        users.append(user_helper(user))
    
    return users
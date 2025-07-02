from database import db
from schemas import user_helper
from models import UserModel, UserUpdateModel
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse

collection = db["users"]

# Funções auxiliares para erros HTTP
def http_400(msg: str):
    return HTTPException(status_code=400, detail=msg)

def http_404(msg: str):
    return HTTPException(status_code=404, detail=msg)

# Criar usuário
async def create_user(user: UserModel):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise http_400("Email já está em uso")
    
    user_data = user.model_dump(by_alias=True, exclude_unset=True)
    user_data["created_at"] = datetime.utcnow()
    
    res = await collection.insert_one(user_data)
    created_user = await collection.find_one({"_id": res.inserted_id})
    return user_helper(created_user)

# Listar usuários com paginação
async def get_users(skip: int = 0, limit: int = 100):
    users = []
    cursor = collection.find().skip(skip).limit(limit)
    async for user in cursor:
        users.append(user_helper(user))
    return users

# Obter usuário por ID
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise http_400("ID de usuário inválido")
    
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise http_404("Usuário não encontrado")
    
    return user_helper(user)

# Atualizar usuário
async def update_user(user_id: str, user_update: UserUpdateModel):
    if not ObjectId.is_valid(user_id):
        raise http_400("ID de usuário inválido")
    
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise http_404("Usuário não encontrado")
    
    if user_update.email:
        email_exists = await collection.find_one({
            "email": user_update.email,
            "_id": {"$ne": ObjectId(user_id)}
        })
        if email_exists:
            raise http_400("Email já está em uso")
    
    update_data = user_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

# Deletar usuário
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise http_400("ID de usuário inválido")
    
    res = await collection.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise http_404("Usuário não encontrado")
    
    return JSONResponse(content={"message": "Usuário deletado com sucesso"}, status_code=200)

# Buscar usuários
async def search_users(query: str, skip: int = 0, limit: int = 100):
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
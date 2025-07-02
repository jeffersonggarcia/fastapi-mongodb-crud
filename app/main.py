from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import UserModel, UserUpdateModel, UserResponse
from crud import create_user, get_users, get_user, update_user, delete_user, search_users
from typing import List
from database import connect_to_mongo, close_mongo_connection  # importe as funções

app = FastAPI(
    title="API CRUD de Usuários",
    description="API RESTful para gerenciamento de usuários com MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "API CRUD de Usuários com FastAPI e MongoDB"}

@app.post("/users", response_model=UserResponse, tags=["Users"])
async def create_new_user(user: UserModel):
    """Criar um novo usuário"""
    return await create_user(user)

@app.get("/users", response_model=List[UserResponse], tags=["Users"])
async def list_users(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar")
):
    """Listar todos os usuários com paginação"""
    return await get_users(skip=skip, limit=limit)

@app.get("/users/search", response_model=List[UserResponse], tags=["Users"])
async def search_users_endpoint(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar")
):
    """Buscar usuários por nome, email ou cidade"""
    return await search_users(query=q, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user_by_id(user_id: str):
    """Obter um usuário específico pelo ID"""
    return await get_user(user_id)

@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user_by_id(user_id: str, user: UserUpdateModel):
    """Atualizar um usuário específico"""
    return await update_user(user_id, user)

@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user_by_id(user_id: str):
    """Deletar um usuário específico"""
    return await delete_user(user_id)

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar se a API está funcionando"""
    return {"status": "healthy", "service": "user-crud-api"}
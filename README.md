# API CRUD de Usuários - FastAPI + MongoDB

Uma API RESTful completa para gerenciamento de usuários usando FastAPI, MongoDB e Docker.

## 🚀 Características

- **FastAPI**: Framework moderno e rápido para APIs Python
- **MongoDB**: Banco de dados NoSQL para armazenamento flexível
- **Docker**: Containerização para fácil deployment
- **Validação de dados**: Validação automática com Pydantic
- **Documentação automática**: Swagger UI e ReDoc
- **CORS**: Configurado para permitir requisições frontend
- **Busca avançada**: Busca por nome, email ou cidade
- **Paginação**: Suporte a paginação nas listagens

## 📋 Funcionalidades

### Endpoints da API

- `POST /users` - Criar novo usuário
- `GET /users` - Listar usuários (com paginação)
- `GET /users/{id}` - Obter usuário por ID
- `PUT /users/{id}` - Atualizar usuário
- `DELETE /users/{id}` - Deletar usuário
- `GET /users/search?q={termo}` - Buscar usuários
- `GET /health` - Health check da API

### Modelo de Usuário

```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "birth_date": "1990-01-15",
  "city": "São Paulo"
}
```

## 🛠️ Tecnologias

- Python 3.13
- FastAPI 0.104.1
- MongoDB (via Motor)
- Docker & Docker Compose
- Pydantic para validação
- Uvicorn como servidor ASGI

## 🚀 Como executar

### Pré-requisitos

- Docker
- Docker Compose

### Executar com Docker

1. Clone o repositório
2. Execute o comando:

```bash
docker-compose up --build
```

3. Acesse a API:
   - API: http://localhost:8000
   - Documentação Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Executar localmente (desenvolvimento)

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente no arquivo `.env`

3. Execute o MongoDB (via Docker):
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

4. Execute a aplicação:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Exemplos de uso

### Criar usuário
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "João Silva",
       "email": "joao@email.com",
       "birth_date": "1990-01-15",
       "city": "São Paulo"
     }'
```

### Listar usuários
```bash
curl "http://localhost:8000/users?skip=0&limit=10"
```

### Buscar usuários
```bash
curl "http://localhost:8000/users/search?q=João&skip=0&limit=10"
```

### Atualizar usuário
```bash
curl -X PUT "http://localhost:8000/users/{user_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "João Santos",
       "city": "Rio de Janeiro"
     }'
```

## 🔧 Configuração

As configurações podem ser ajustadas através de variáveis de ambiente no arquivo `.env`:

```env
MONGO_URL=mongodb://mongodb:27017
DATABASE_NAME=userdb
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
DEBUG=true
```

## 📁 Estrutura do projeto

```
fastapi-mongodb-crud/
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicação FastAPI principal
│   ├── models.py        # Modelos Pydantic
│   ├── crud.py          # Operações CRUD
│   ├── database.py      # Configuração do MongoDB
│   ├── schemas.py       # Schemas de resposta
│   └── config.py        # Configurações da aplicação
├── docker-compose.yml   # Configuração Docker Compose
├── Dockerfile          # Configuração Docker
├── requirements.txt    # Dependências Python
├── .env               # Variáveis de ambiente
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Documentação
```

## 🧪 Validações implementadas

- **Email**: Validação de formato de email
- **Data de nascimento**: Não pode ser no futuro
- **Nome e cidade**: Não podem estar vazios, são capitalizados automaticamente
- **Email único**: Evita duplicação de emails
- **IDs MongoDB**: Validação de ObjectId válidos

## 🚧 Melhorias futuras

- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Logs estruturados
- [ ] Testes automatizados
- [ ] Cache com Redis
- [ ] Métricas e monitoramento
- [ ] Versionamento da API

## 📄 Licença

Este projeto está sob a licença MIT.

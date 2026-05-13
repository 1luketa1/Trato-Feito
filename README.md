# Trato-Feito

pip install neo4j

pip install fastapi

pip install uvicorn

pip install pymongo

pip install requests

pip install python-dotenv

pip install redis

COMANDOS PARA RODAR O PROJETO

1. LIGAR O REDIS (Docker)

docker start redis-tf

Verificar se está rodando:

docker ps


2. LIGAR A API (FastAPI)

python -m uvicorn api:app --reload

Quando estiver funcionando, deve aparecer:

Uvicorn running on http://127.0.0.1:8000


3. RODAR O APP PRINCIPAL

Em outro terminal:

python main.py

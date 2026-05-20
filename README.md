# Trato-Feito

Sistema de apostas em corridas de cavalos desenvolvido para a disciplina CCD410.

---

## Tema do Projeto

O projeto "Trato-Feito" simula uma plataforma de apostas em corridas de cavalos, onde usuários podem:

- Criar conta e fazer login
- Depositar e sacar dinheiro
- Visualizar corridas disponíveis
- Apostar em cavalos
- Simular corridas
- Receber prêmios com base nas odds


---

## Arquitetura e Bancos de Dados

### Redis

Utilizado como banco principal da aplicação.

Funções:
- Armazenamento de usuários
- Controle de saldo
- Armazenamento de tickets (apostas)
- Persistência em JSON

Justificativa:
Redis foi escolhido por ser rápido e eficiente para operações frequentes como leitura e escrita de saldo e apostas.

---

### MongoDB

Utilizado para armazenar dados estruturados da aplicação.

Funções:
- Corridas
- Cavalos
- Pistas

Justificativa:
MongoDB permite trabalhar com documentos flexíveis, facilitando o armazenamento de estruturas complexas como corridas com múltiplos cavalos.

---

### Neo4j

Utilizado para análise de relações entre entidades.

Funções:
- Relação entre usuários, apostas, corridas e cavalos
- Possível recomendação de apostas

Justificativa:
Neo4j é adequado para representar relações complexas em forma de grafo.

---

## Backend

O backend foi implementado utilizando:

- FastAPI para criação da API
- Uvicorn como servidor

A API é responsável por:
- Gerenciar corridas
- Simular resultados
- Fornecer dados para o frontend (Tkinter)

---

## Como Executar o Projeto

### 1. Instalar dependências

pip install neo4j  
pip install fastapi  
pip install uvicorn  
pip install pymongo  
pip install requests  
pip install python-dotenv  
pip install redis  

---

### 2. Configurar o .env

O arquivo .env é necessário para conexão com o MongoDB.

O conteúdo foi enviado separadamente por email.

O assunto do Email é ( Conteúdo do .env CCD410 do grupo 38 )

---

### 3. Iniciar o Redis (Docker)

Instalar o Docker:  
https://www.docker.com/products/docker-desktop/

Primeira execução:

docker run -d -p 6379:6379 --name redis-tf redis

Execuções seguintes:

docker start redis-tf

Verificar se está rodando:

docker ps

---

### 4. Iniciar a API

python -m uvicorn api:app --reload

Deve aparecer:

Uvicorn running on http://127.0.0.1:8000

---

### 5. Executar o sistema

Em outro terminal:

python main.py

---

## Observações

- Redis é essencial para funcionamento do sistema
- MongoDB é necessário via .env

---

## Autores

Caio Henrique De Oliveira Fonseca - 24124066-2

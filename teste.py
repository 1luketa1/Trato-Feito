#NÃO ESQUECER DE ABRIR O SERVIDOR NO TERMINAL server (comando é 'redis-server') !!!!!!!
#FECHAR COM CTRL C

import redis
import json

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

def criarUsuario(nome, senha):

    usuarioId = r.incr("proximoUsuarioId")

    r.hset(f"usuario:{usuarioId}", mapping={
        "id": usuarioId,
        "nome": nome,
        "senha": senha,
        "saldo": 0
    })

criarUsuario("Carlos", "banana123")
criarUsuario("Célia", "441")
criarUsuario("Cleber", "sixSeven")

usuarios = []

for chave in r.keys("usuario:*"):
    dados = r.hgetall(chave)
    usuarios.append(dados)

with open("usuarios.json", "w", encoding = "utf-8") as arquivo:

    json.dump(
        usuarios,
        arquivo,
        indent=4,
        ensure_ascii=False
    )

print("Arquivo JSON criado!")

#Teste de print dos usuários
    # ultimoId = int(r.get("proximoUsuarioId"))

    # for i in range(1, ultimoId +1):
    #     dados = r.hgetall(f"usuario:{i}")
    #     print(dados)
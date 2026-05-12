#NÃO ESQUECER DE ABRIR O SERVIDOR NO TERMINAL server (comando é 'redis-server') !!!!!!!
#FECHAR COM CTRL C

import redis
import json


r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)



#FUNÇÕES
def criarUsuario(nome, senha):
    for chave in r.keys("usuario:*"):
        usuario = r.hgetall(chave)
        if usuario["nome"].lower() == nome.lower():
            print("Já existe um usuário com este nome, tente novamente")
            return
        
    usuarioId = r.incr("proximoUsuarioId")

    r.hset(f"usuario:{usuarioId}", mapping={
        "id": usuarioId,
        "nome": nome,
        "senha": senha,
        "saldo": 0
    })

def atualizarUsuario(usuarioId, novosDados):

    chave = f"usuario:{usuarioId}"

    if not r.exists(chave):

        print("Usuário não encontrado")
        return

    r.hset(chave, mapping=novosDados)

    print("Usuário atualizado")

def salvarUsuario(usuarioId):
    usuarios = []

    if usuarioId == "*":
        for chave in r.keys("usuario:*"):
            dados = r.hgetall(chave)
            usuarios.append(dados)
    else:
        chave = f"usuario:{usuarioId}"
        if not r.exists(chave):

            print("Usuário não encontrado")
            return
        else:
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

def deletarUsuario(usuarioId):

    chave = f"usuario:{usuarioId}"

    # verifica existência
    if not r.exists(chave):

        print("Usuário não encontrado")
        return

    r.delete(chave)
    salvarUsuario("*")
    print("Usuário deletado")

#SOB NENHUMA INSTÂNCIA USAR ISSO NO PROGRAMA DE VERDADE, É APENAS PARA DEBUGGAR
def limpaBanco():
     r.flushdb()
#fim das funções

#limpaBanco()
#criarUsuario("Carlos", "banana123")
#salvarUsuario(2)
deletarUsuario(2)

#Teste de print dos usuários
ultimoId = int(r.get("proximoUsuarioId"))
for i in range(1, ultimoId +1):
    dados = r.hgetall(f"usuario:{i}")
    print(dados)
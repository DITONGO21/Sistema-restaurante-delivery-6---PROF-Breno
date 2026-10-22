from server.connection_server import conectar_bd
from server.autenticação import (
    registar_utilizador,
    autenticar_utilizador
)

mybd = conectar_bd()
mycursor = mybd.cursor()

if mybd and mycursor:
    nome = "teste_hash"
    password = "Senha123!"

    # Testar o registo
    registado = registar_utilizador(
        mybd, mycursor, nome, password, "cliente"
    )

    print("Registo:", registado)

    # Testar o login correto
    login_correto = autenticar_utilizador(
        mycursor, nome, password
    )
    print("Password correta:", login_correto)

    # Testar o login errado
    login_errado = autenticar_utilizador(
        mycursor, nome, "password_errada"
    )
    print("Password errada:", login_errado)

    mycursor.close()
    mybd.close()
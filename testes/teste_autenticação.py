from server.connection_server import conectar_bd
from server.autenticação import (
    registar_utilizador,
    autenticar_utilizador
)


conexao = conectar_bd()

if conexao is None:
    print("Não foi possível ligar à base de dados.")
    raise SystemExit

cursor = conexao.cursor(dictionary=True)

try:
    nome = input("Nome de utilizador para testar: ")
    password = input("Palavra-passe para testar: ")

    registado = registar_utilizador(
        conexao, cursor, nome, password, "cliente"
    )

    if registado:
        print("Registo efetuado com sucesso!")
    else:
        print("Registo não efetuado. O nome pode já existir ou ocorreu um erro.")

    password_login = input("Introduz a palavra-passe para testar o login: ")

    if autenticar_utilizador(cursor, nome, password_login):
        print("Login correto!")
    else:
        print("Login incorreto!")

finally:
    cursor.close()
    conexao.close()

import bcrypt

from server.base_de_dados import (
    Consultar_utilizador,
    Impedir_Duplicados,
    Registrar_utilizadores
)

def criar_hash(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verificar_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

def registar_utilizador(mybd, mycursor, nome, password, tipo):
    if Impedir_Duplicados(mycursor, nome):
        return False

    password_hash = criar_hash(password)

    return Registrar_utilizadores(
        mybd, mycursor, nome, password_hash, tipo
    )

def autenticar_utilizador(mycursor, nome, password):
    utilizador = Consultar_utilizador(mycursor, nome)

    if utilizador is None:
        return False

    password_hash = utilizador[2]  # Supondo que a password_hash está na terceira coluna do resultado da consulta

    return verificar_password(password, password_hash)

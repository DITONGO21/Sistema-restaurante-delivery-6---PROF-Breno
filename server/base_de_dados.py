import mysql.connector
from connection_server import conectar_bd

def Registrar_utilizadores(mybd, mycursor, nome, password_hash, tipo):
    try:
        sql = "INSERT INTO utilizadores (nome_utilizador, password_hash, tipo_utilizador) VALUES (%s, %s, %s)"
        mycursor.execute(sql, (nome, password_hash, tipo))
        mybd.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao registrar utilizador: {err}")
        mybd.rollback()
        return False

def Consultar_utilizador(mycursor, nome):
    try:
        sql = "SELECT * FROM utilizadores WHERE nome_utilizador = %s"
        mycursor.execute(sql, (nome,))
        return mycursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Erro ao consultar utilizador: {err}")
        return None

def Consultar_produtos(mycursor,nome):
    try:
        sql="SELECT * FROM produtos WHERE nome = %s"
        mycursor.execute(sql, (nome,))
        return mycursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Erro ao consultar produto: {err}")
        return None

def Criar_pedidos(mybd, mycursor, id_utilizador, id_produto, quantidade):
    try:
        sql = "INSERT INTO pedidos (id_utilizador, id_produto, quantidade) VALUES (%s, %s, %s)"
        mycursor.execute(sql, (id_utilizador, id_produto, quantidade))
        mybd.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao criar pedido: {err}")
        mybd.rollback()
        return False


    
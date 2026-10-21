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

def Atualizar_stock(mybd, mycursor, id_produto, nova_quantidade):
    try:
        sql = "UPDATE produtos SET stock = %s WHERE id_produto = %s"
        mycursor.execute(sql, (nova_quantidade, id_produto))
        mybd.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar o stock: {err}")
        mybd.rollback()
        return False

def Consultar_historico_pedidos(mycursor, id_utilizador):
    try:
        sql = "SELECT * FROM pedidos WHERE id_utilizador = %s"
        mycursor.execute(sql, (id_utilizador,))
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao consultar historico: {err}")
        return None
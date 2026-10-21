
import mysql.connector


def Registrar_utilizadores(mybd, mycursor, nome, password_hash, tipo):
    try:
        sql = """
            INSERT INTO utilizadores
            (nome_utilizador, password_hash, tipo_utilizador)
            VALUES (%s, %s, %s)
        """
        mycursor.execute(sql, (nome, password_hash, tipo))
        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao registar utilizador: {erro}")
        mybd.rollback()
        return False


def Consultar_utilizador(mycursor, nome):
    try:
        sql = """
            SELECT * FROM utilizadores
            WHERE nome_utilizador = %s
        """
        mycursor.execute(sql, (nome,))
        return mycursor.fetchone()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar utilizador: {erro}")
        return None


def Consultar_produtos(mycursor, nome):
    try:
        sql = "SELECT * FROM produtos WHERE nome = %s"
        mycursor.execute(sql, (nome,))
        return mycursor.fetchone()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar produto: {erro}")
        return None


def Criar_pedidos(mybd, mycursor, id_utilizador, id_produto, quantidade):
    try:
        sql = """
            INSERT INTO pedidos
            (id_utilizador, id_produto, quantidade)
            VALUES (%s, %s, %s)
        """
        mycursor.execute(sql, (id_utilizador, id_produto, quantidade))
        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao criar pedido: {erro}")
        mybd.rollback()
        return False


def Atualizar_stock(mybd, mycursor, id_produto, nova_quantidade):
    try:
        if nova_quantidade < 0:
            print("O stock não pode ser negativo.")
            return False

        sql = """
            UPDATE produtos
            SET stock = %s
            WHERE id_produto = %s
        """
        mycursor.execute(sql, (nova_quantidade, id_produto))

        if mycursor.rowcount == 0:
            mybd.rollback()
            print("Produto não encontrado ou stock inalterado.")
            return False

        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar o stock: {erro}")
        mybd.rollback()
        return False


def Consultar_historico_pedidos(mycursor, id_utilizador):
    try:
        sql = """
            SELECT * FROM pedidos
            WHERE id_utilizador = %s
        """
        mycursor.execute(sql, (id_utilizador,))
        return mycursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar histórico: {erro}")
        return None

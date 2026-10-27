import mysql.connector

VALID_ESTADOS_PEDIDO = {
    "pendente",
    "em preparacao",
    "em entrega",
    "entregue",
    "cancelado",
}


def validar_estado_pedido(estado):
    if not isinstance(estado, str):
        return False
    return estado.strip().lower() in VALID_ESTADOS_PEDIDO


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
            SELECT *
            FROM utilizadores
            WHERE nome_utilizador = %s
        """

        mycursor.execute(sql, (nome,))
        return mycursor.fetchone()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar utilizador: {erro}")
        return None


def Impedir_Duplicados(mycursor, nome):
    try:
        sql = """
            SELECT 1
            FROM utilizadores
            WHERE nome_utilizador = %s
            LIMIT 1
        """

        mycursor.execute(sql, (nome,))
        return mycursor.fetchone() is not None

    except mysql.connector.Error as erro:
        print(f"Erro ao verificar utilizador duplicado: {erro}")
        return True


def Consultar_produtos(mycursor, nome=""):
    try:
        if nome:
            sql = """
                SELECT *
                FROM produtos
                WHERE nome LIKE %s
            """

            mycursor.execute(sql, (f"%{nome}%",))
        else:
            sql = "SELECT * FROM produtos"
            mycursor.execute(sql)

        return mycursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar produtos: {erro}")
        return []


def Adicionar_produto(
    mybd,
    mycursor,
    nome,
    descricao,
    categoria,
    preco,
    stock,
):
    try:
        mycursor.execute(
            """
            INSERT INTO produtos (nome, descricao, categoria, preco, stock)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, descricao, categoria, preco, stock),
        )
        id_produto = mycursor.lastrowid
        mybd.commit()
        return id_produto

    except mysql.connector.Error as erro:
        print(f"Erro ao adicionar produto: {erro}")
        mybd.rollback()
        return None


def Criar_pedidos(mybd, mycursor, id_utilizador, id_produto, quantidade):
    try:
        if (
            not isinstance(quantidade, int)
            or isinstance(quantidade, bool)
            or quantidade <= 0
        ):
            return False

        # Consultar produto e stock
        mycursor.execute(
            """
            SELECT preco, stock
            FROM produtos
            WHERE id_produto = %s
            FOR UPDATE
            """,
            (id_produto,)
        )

        produto = mycursor.fetchone()

        if produto is None:
            print("Produto não encontrado.")
            mybd.rollback()
            return False

        preco = produto[0]
        stock = produto[1]

        if stock < quantidade:
            print("Stock insuficiente.")
            mybd.rollback()
            return False

        valor_total = preco * quantidade

        # Criar pedido
        mycursor.execute(
            """
            INSERT INTO pedidos (id_cliente, valor_total)
            VALUES (%s, %s)
            """,
            (id_utilizador, valor_total)
        )

        id_pedido = mycursor.lastrowid

        # Inserir detalhes do pedido
        mycursor.execute(
            """
            INSERT INTO detalhes_pedido
            (id_pedido, id_produto, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
            """,
            (id_pedido, id_produto, quantidade, preco)
        )

        # Atualizar stock
        mycursor.execute(
            """
            UPDATE produtos
            SET stock = stock - %s
            WHERE id_produto = %s
            """,
            (quantidade, id_produto)
        )

        mybd.commit()
        return id_pedido

    except mysql.connector.Error as erro:
        mybd.rollback()
        print(f"Erro ao criar pedido: {erro}")
        return False


def Atualizar_stock(mybd, mycursor, id_produto, nova_quantidade):
    try:
        if (
            not isinstance(nova_quantidade, int)
            or isinstance(nova_quantidade, bool)
            or nova_quantidade < 0
        ):
            print("O stock tem de ser um número inteiro igual ou superior a zero.")
            return False

        sql = """
            UPDATE produtos
            SET stock = %s
            WHERE id_produto = %s
        """

        mycursor.execute(sql, (nova_quantidade, id_produto))

        if mycursor.rowcount == 0:
            mycursor.execute(
                "SELECT 1 FROM produtos WHERE id_produto = %s",
                (id_produto,),
            )
            if mycursor.fetchone() is None:
                mybd.rollback()
                print("Produto não encontrado.")
                return False

        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar o stock: {erro}")
        mybd.rollback()
        return False


def Consultar_historico_pedidos(mycursor, id_utilizador):
    try:
        mycursor.execute(
            """
            SELECT *
            FROM pedidos
            WHERE id_cliente = %s
            ORDER BY data_pedido DESC
            """,
            (id_utilizador,)
        )

        return mycursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar histórico: {erro}")
        return None


def Consultar_pedidos(mycursor):
    try:
        mycursor.execute(
            """
            SELECT p.id_pedido, p.id_cliente, u.nome_utilizador,
                   p.data_pedido, p.estado, p.valor_total
            FROM pedidos AS p
            JOIN utilizadores AS u
              ON u.id_utilizador = p.id_cliente
            ORDER BY p.data_pedido DESC, p.id_pedido DESC
            """
        )
        return mycursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar pedidos: {erro}")
        return None


def Consultar_entregas(mycursor, id_entregador):
    try:
        mycursor.execute(
            """
            SELECT p.id_pedido, u.nome_utilizador, p.data_pedido,
                   p.estado, p.valor_total, p.id_entregador
            FROM pedidos AS p
            JOIN utilizadores AS u
              ON u.id_utilizador = p.id_cliente
            WHERE p.estado = 'pendente'
               OR (p.id_entregador = %s AND p.estado = 'em entrega')
            ORDER BY p.data_pedido ASC, p.id_pedido ASC
            """,
            (id_entregador,),
        )
        return mycursor.fetchall()

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar entregas: {erro}")
        return None


def Aceitar_entrega(mybd, mycursor, id_pedido, id_entregador):
    try:
        mycursor.execute(
            """
            UPDATE pedidos
            SET id_entregador = %s, estado = 'em entrega'
            WHERE id_pedido = %s
              AND estado = 'pendente'
              AND id_entregador IS NULL
            """,
            (id_entregador, id_pedido),
        )
        if mycursor.rowcount != 1:
            mybd.rollback()
            return False

        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao aceitar entrega: {erro}")
        mybd.rollback()
        return False


def Atualizar_estado_entrega(mybd, mycursor, id_pedido, id_entregador, estado):
    if estado != "entregue":
        return False

    try:
        mycursor.execute(
            """
            UPDATE pedidos
            SET estado = %s
            WHERE id_pedido = %s
              AND id_entregador = %s
              AND estado = 'em entrega'
            """,
            (estado, id_pedido, id_entregador),
        )
        if mycursor.rowcount != 1:
            mybd.rollback()
            return False

        mybd.commit()
        return True

    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar estado da entrega: {erro}")
        mybd.rollback()
        return False

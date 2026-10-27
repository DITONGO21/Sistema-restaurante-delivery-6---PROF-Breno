from server.base_de_dados import Criar_pedidos

def criar_pedido(conexao, cursor, id_utilizador, id_produto, quantidade):
    if (
        not isinstance(id_utilizador, int)
        or isinstance(id_utilizador, bool)
        or id_utilizador <= 0
    ):
        return{
            "estado": "erro",
            "mensagem": "ID do cliente invalido",
            "dados": {},
        }

    if (
        not isinstance(id_produto, int)
        or isinstance(id_produto, bool)
        or id_produto <= 0
    ):
        return{
            "estado": "erro",
            "mensagem": "ID do produto errado",
            "dados": {},
        }

    if (
        not isinstance(quantidade, int)
        or isinstance(quantidade, bool)
        or quantidade <= 0
    ):
        return {
            "estado": "erro",
            "mensagem": "A quantidade tem de ser superior a zero.",
            "dados": {},
        }

    cursor.execute(
    """
    SELECT id_utilizador
    from utilizadores
    WHERE id_utilizador = %s
        AND tipo_utilizador = 'cliente'
    """,
    (id_utilizador,),
    )

    if cursor.fetchone() is None:
        return {
            "estado": "erro",
            "mensagem": "Cliente não encontrado.",
            "dados": {},
        }

    id_pedido = Criar_pedidos(
        conexao,
        cursor,
        id_utilizador,
        id_produto,
        quantidade,
    )

    if not id_pedido:
        return {
            "estado": "erro",
            "mensagem": "Não foi possível criar o pedido. Verifica o produto e o stock.",
            "dados": {},
        }

    return {
        "estado": "sucesso",
        "mensagem": "Pedido criado com sucesso.",
        "dados": {
            "id_pedido": id_pedido,
        },
    }
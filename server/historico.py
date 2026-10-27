from server.base_de_dados import Consultar_historico_pedidos


def consultar_historico(cursor, id_utilizador):
    """Consulta o histórico de pedidos de um cliente."""

    if (
        not isinstance(id_utilizador, int)
        or isinstance(id_utilizador, bool)
        or id_utilizador <= 0
    ):
        return {
            "estado": "erro",
            "mensagem": "ID do cliente inválido.",
            "dados": {},
        }

    cursor.execute(
        """
        SELECT id_utilizador
        FROM utilizadores
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

    pedidos = Consultar_historico_pedidos(cursor, id_utilizador)

    if pedidos is None:
        return {
            "estado": "erro",
            "mensagem": "Erro ao consultar o histórico.",
            "dados": {},
        }

    return {
        "estado": "sucesso",
        "mensagem": "Histórico consultado.",
        "dados": {
            "pedidos": [list(pedido) for pedido in pedidos]
        },
    }
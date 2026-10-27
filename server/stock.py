from server.base_de_dados import Atualizar_stock


def atualizar_stock(conexao, cursor, id_produto, nova_quantidade):
    if (
        not isinstance(id_produto, int)
        or isinstance(id_produto, bool)
        or id_produto <= 0
    ):
        return {
            "estado": "erro",
            "mensagem": "ID do produto inválido.",
            "dados": {},
        }

    if (
        not isinstance(nova_quantidade, int)
        or isinstance(nova_quantidade, bool)
        or nova_quantidade < 0
    ):
        return {
            "estado": "erro",
            "mensagem": "O stock tem de ser um inteiro igual ou superior a zero.",
            "dados": {},
        }

    cursor.execute(
        "SELECT id_produto FROM produtos WHERE id_produto = %s",
        (id_produto,),
    )

    if cursor.fetchone() is None:
        return {
            "estado": "erro",
            "mensagem": "Produto não encontrado.",
            "dados": {},
        }

    sucesso = Atualizar_stock(
        conexao,
        cursor,
        id_produto,
        nova_quantidade,
    )

    if not sucesso:
        return {
            "estado": "erro",
            "mensagem": "Não foi possível atualizar o stock.",
            "dados": {},
        }

    return {
        "estado": "sucesso",
        "mensagem": "Stock atualizado com sucesso.",
        "dados": {
            "id_produto": id_produto,
            "stock": nova_quantidade,
        },
    }
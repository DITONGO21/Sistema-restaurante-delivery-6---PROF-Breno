from server.base_de_dados import Consultar_produtos

def listar_produtos(cursor, nome=None):
    """Devolve a lista de produtos, opcionalmente filtrada pelo nome."""
    try:
        produtos = Consultar_produtos(cursor)
        if produtos is None:
            produtos = []

        if nome:
            nome = str(nome).strip().lower()
            produtos = [
                produto for produto in produtos
                if nome in str(produto[1]).lower()
            ]

        return {
            "estado": "sucesso",
            "mensagem": "Produtos encontrados" if produtos else "Não existem produtos.",
            "dados": {"produtos": produtos},
        }

    except Exception as erro:
        print(f"Erro ao listar produtos: {erro}")
        return {
            "estado": "erro",
            "mensagem": "Não foi possível consultar os produtos.",
            "dados": {},
        }

from cliente.connection_clientes import enviar_pedido


def listar_produtos(nome=""):
    return enviar_pedido("listar_produtos", {"nome": nome})


def registar_utilizador(nome, password, tipo="cliente"):
    return enviar_pedido(
        "registar",
        {
            "nome": nome,
            "password": password,
            "tipo": tipo
        }
    )


def login_utilizador(nome, password):
    return enviar_pedido(
        "login",
        {
            "nome": nome,
            "password": password,
        }
    )


def criar_pedido(id_utilizador, id_produto, quantidade):
    return enviar_pedido(
        "criar_pedido",
        {
            "id_utilizador": id_utilizador,
            "id_produto": id_produto,
            "quantidade": quantidade
        }
    )


def consultar_historico(id_utilizador):
    return enviar_pedido(
        "historico_pedidos",
        {"id_utilizador": id_utilizador}
    )


def gerir_stock(id_utilizador, id_produto, stock):
    return enviar_pedido(
        "gerir_stock",
        {
            "id_utilizador": id_utilizador,
            "id_produto": id_produto,
            "stock": stock,
        },
    )


def consultar_pedidos(id_utilizador):
    return enviar_pedido(
        "consultar_pedidos",
        {"id_utilizador": id_utilizador},
    )


def consultar_entregas(id_utilizador):
    return enviar_pedido(
        "consultar_entregas",
        {"id_utilizador": id_utilizador},
    )


def aceitar_entrega(id_utilizador, id_pedido):
    return enviar_pedido(
        "aceitar_entrega",
        {"id_utilizador": id_utilizador, "id_pedido": id_pedido},
    )


def concluir_entrega(id_utilizador, id_pedido):
    return enviar_pedido(
        "atualizar_estado_entrega",
        {
            "id_utilizador": id_utilizador,
            "id_pedido": id_pedido,
            "estado": "entregue",
        },
    )
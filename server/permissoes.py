tipo_utilizador = ("cliente", "entregador", "admin")

permissoes = {
    "cliente": (
        "listar_produtos",
        "criar_pedido",
        "historico_pedidos",
    ),

    "entregador": (
        "consultar_entregas",
        "aceitar_entrega",
        "atualizar_estado_entrega",
    ),

    "admin": (
        "listar_produtos",
        "gerir_produtos",
        "gerir_utilizadores",
        "consultar_pedidos",
        "gerir_stock",
    ),
}

def validar_tipo_utilizador(tipo):
    return tipo in tipo_utilizador

validar_tipo_utilizador("cliente")

def tem_permissao(tipo, operacao):
    """Verifica se um tipo de utilizador pode executar uma operação."""
    if not validar_tipo_utilizador(tipo):
        return False

    return operacao in permissoes.get(tipo, ())

def verificar_identidade(utilizador, id_utilizador):

    if not isinstance(utilizador, dict):
        return False

    if not isinstance(id_utilizador, int) or isinstance(id_utilizador, bool):
        return False

    return utilizador.get("id_utilizador") == id_utilizador
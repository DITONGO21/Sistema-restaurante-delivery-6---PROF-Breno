from server.menu_service import listar_produtos
from comum.protocologo import criar_resposta

def processar_requisicao(mensagem, cursor=None, conexao=None):
    """Valida a mensagem e encaminha a operação correspondente."""
    if not isinstance(mensagem, dict):
        return criar_resposta(
            "erro", "Mensagem inválida", {}
        )

    operacao = mensagem.get("operacao")
    dados = mensagem.get("dados", {})

    if not isinstance(operacao, str) or not isinstance(dados, dict):
        return criar_resposta(
            "erro", "Operação ou dados invalidos", {}
        )

    if operacao == "listar_produtos":
        if cursor is None:
            return criar_resposta(
                "erro", "Base de dados indisponível", {}
            )

        resultado = listar_produtos(cursor, dados.get("nome"))
        return criar_resposta(
            resultado["estado"],
            resultado["mensagem"],
            resultado["dados"],
        )

    return criar_resposta(
        "erro",
        "Operação não funciono",
        {},
    )
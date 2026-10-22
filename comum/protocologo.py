import json

def criar_mensagem(operacao, dados):
    """Cria uma mensagem JSON para comunicação entre cliente e servidor."""

    mensagem = {
        "operacao": operacao,
        "dados": dados or {}
    }

    return json.dumps(mensagem, ensure_ascii=False) # server para converter para JSON e enviar para o cliente, ensure_ascii=False para permitir caracteres especiais

def ler_mensagem(mensagem):
    """Converte uma mensagem JSON recebida em um dicionário Python."""

    try:
        dados = json.loads(mensagem)

        if not isinstance(dados, dict):
            return None

        if "operacao" not in dados:
            return None

        if not isinstance(dados.get("dados", {}), dict):
            return None

        return dados

    except (json.JSONDecodeError, TypeError):
        return None

def criar_resposta(estado, mensagem="", dados = None):
    """Cria uma resposta do servidor para o cliente"""

    resposta = {
        "estado": estado,
        "mensagem": mensagem,
        "dados": dados or {}
    }

    return json.dumps(resposta, ensure_ascii=False)
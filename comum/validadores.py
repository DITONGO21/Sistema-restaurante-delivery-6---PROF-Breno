def campo_obrigatorio(valor):
    if valor is None or str(valor).strip() == "":
        return False
    return True

def validar_quantidade(quantidade):
    if isinstance(quantidade, int) and not isinstance(quantidade, bool):
        if quantidade > 0:
            return True
        return False

def validar_preco(preco):
    try:
        preco = float(preco)

        if preco >= 0 and preco != float("inf") and preco == preco:
            return True
        else:
            return False

    except (ValueError, TypeError):
        return False

def validar_produto(nome, preco, stock):
    if not campo_obrigatorio(nome):
        return False

    if not validar_preco(preco):
        return False

    if not validar_quantidade(stock):
        return False
    return True

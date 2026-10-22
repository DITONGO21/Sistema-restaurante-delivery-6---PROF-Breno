
import math


def campo_obrigatorio(valor):
    if valor is None or str(valor).strip() == "":
        return False
    return True


def validar_quantidade(quantidade):
    return (
        isinstance(quantidade, int)
        and not isinstance(quantidade, bool)
        and quantidade > 0
    )


def validar_preco(preco):
    try:
        preco = float(preco)
        return math.isfinite(preco) and preco >= 0
    except (ValueError, TypeError):
        return False


def validar_stock(stock):
    return (
        isinstance(stock, int)
        and not isinstance(stock, bool)
        and stock >= 0
    )


def validar_produto(nome, preco, stock):
    if not campo_obrigatorio(nome):
        return False

    if not validar_preco(preco):
        return False

    if not validar_stock(stock):
        return False

    return True

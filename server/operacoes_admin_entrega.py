from decimal import Decimal, InvalidOperation

from server.base_de_dados import (
    Adicionar_produto,
    Aceitar_entrega,
    Atualizar_estado_entrega,
    Atualizar_stock,
    Consultar_entregas,
    Consultar_pedidos,
)

def _id_inteiro_positivo(valor):
    return (
        isinstance(valor, int)
        and not isinstance(valor, bool)
        and valor > 0
    )

def _validar_tipo_utilizador(cursor, id_utilizador, tipo):
    if not _id_inteiro_positivo(id_utilizador):
        return False

    cursor.execute(
        """
        SELECT id_utilizador
        FROM utilizadores
        WHERE id_utilizador = %s AND tipo_utilizador = %s
        """,
        (id_utilizador, tipo),
    )
    return cursor.fetchone() is not None

def processar_operacao_admin_entrega(operacao, dados, conexao, cursor):
    id_utilizador = dados.get("id_utilizador")

    if operacao == "adicionar_produto":
        if not _id_inteiro_positivo(id_utilizador) or not _validar_tipo_utilizador(
            cursor, id_utilizador, "admin"
        ):
            return {
                "estado": "erro",
                "mensagem": "Administrador não encontrado.",
                "dados": {},
            }

        nome = dados.get("nome")
        descricao = dados.get("descricao", "")
        categoria = dados.get("categoria")
        preco = dados.get("preco")
        stock = dados.get("stock")

        if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
            return {
                "estado": "erro",
                "mensagem": "O nome é obrigatório e pode ter até 100 caracteres.",
                "dados": {},
            }
        if not isinstance(descricao, str):
            return {
                "estado": "erro",
                "mensagem": "A descrição tem de ser texto.",
                "dados": {},
            }
        if (
            not isinstance(categoria, str)
            or not categoria.strip()
            or len(categoria.strip()) > 50
        ):
            return {
                "estado": "erro",
                "mensagem": "A categoria é obrigatória e pode ter até 50 caracteres.",
                "dados": {},
            }
        if (
            not isinstance(stock, int)
            or isinstance(stock, bool)
            or stock < 0
        ):
            return {
                "estado": "erro",
                "mensagem": "O stock tem de ser um inteiro igual ou superior a zero.",
                "dados": {},
            }

        try:
            preco_decimal = Decimal(str(preco))
        except (InvalidOperation, ValueError):
            preco_decimal = Decimal("NaN")

        if (
            isinstance(preco, bool)
            or not preco_decimal.is_finite()
            or preco_decimal < 0
            or preco_decimal > Decimal("99999999.99")
            or preco_decimal != preco_decimal.quantize(Decimal("0.01"))
        ):
            return {
                "estado": "erro",
                "mensagem": "O preço tem de ser válido, não negativo e ter no máximo duas casas decimais.",
                "dados": {},
            }

        id_produto = Adicionar_produto(
            conexao,
            cursor,
            nome.strip(),
            descricao.strip(),
            categoria.strip(),
            preco_decimal,
            stock,
        )
        if id_produto is None:
            return {
                "estado": "erro",
                "mensagem": "Não foi possível adicionar o produto.",
                "dados": {},
            }

        return {
            "estado": "sucesso",
            "mensagem": "Produto adicionado com sucesso.",
            "dados": {"id_produto": id_produto},
        }

    if operacao == "gerir_stock":
        id_produto = dados.get("id_produto")
        stock = dados.get("stock")

        if not _id_inteiro_positivo(id_utilizador) or not _validar_tipo_utilizador(
            cursor, id_utilizador, "admin"
        ):
            return {
                "estado": "erro",
                "mensagem": "Administrador não encontrado.",
                "dados": {},
            }
        if not _id_inteiro_positivo(id_produto):
            return {
                "estado": "erro",
                "mensagem": "ID do produto inválido.",
                "dados": {},
            }
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
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
        if not Atualizar_stock(conexao, cursor, id_produto, stock):
            return {
                "estado": "erro",
                "mensagem": "Não foi possível atualizar o stock.",
                "dados": {},
            }

        return {
            "estado": "sucesso",
            "mensagem": "Stock atualizado com sucesso.",
            "dados": {"id_produto": id_produto, "stock": stock},
        }

    if operacao == "consultar_pedidos":
        if not _id_inteiro_positivo(id_utilizador) or not _validar_tipo_utilizador(
            cursor, id_utilizador, "admin"
        ):
            return {
                "estado": "erro",
                "mensagem": "Administrador não encontrado.",
                "dados": {},
            }

        pedidos = Consultar_pedidos(cursor)
        if pedidos is None:
            return {
                "estado": "erro",
                "mensagem": "Erro ao consultar pedidos.",
                "dados": {},
            }
        return {
            "estado": "sucesso",
            "mensagem": "Pedidos consultados.",
            "dados": {"pedidos": [list(pedido) for pedido in pedidos]},
        }

    if operacao == "consultar_entregas":
        if not _id_inteiro_positivo(id_utilizador) or not _validar_tipo_utilizador(
            cursor, id_utilizador, "entregador"
        ):
            return {
                "estado": "erro",
                "mensagem": "Entregador não encontrado.",
                "dados": {},
            }

        entregas = Consultar_entregas(cursor, id_utilizador)
        if entregas is None:
            return {
                "estado": "erro",
                "mensagem": "Erro ao consultar entregas.",
                "dados": {},
            }
        return {
            "estado": "sucesso",
            "mensagem": "Entregas consultadas.",
            "dados": {"entregas": [list(entrega) for entrega in entregas]},
        }

    if operacao in {"aceitar_entrega", "atualizar_estado_entrega"}:
        if not _id_inteiro_positivo(id_utilizador) or not _validar_tipo_utilizador(
            cursor, id_utilizador, "entregador"
        ):
            return {
                "estado": "erro",
                "mensagem": "Entregador não encontrado.",
                "dados": {},
            }

        id_pedido = dados.get("id_pedido")
        if not _id_inteiro_positivo(id_pedido):
            return {
                "estado": "erro",
                "mensagem": "ID do pedido inválido.",
                "dados": {},
            }

        if operacao == "aceitar_entrega":
            sucesso = Aceitar_entrega(conexao, cursor, id_pedido, id_utilizador)
            mensagem = (
                "Entrega aceite com sucesso."
                if sucesso
                else "Pedido indisponível para entrega."
            )
        else:
            estado = dados.get("estado")
            if estado != "entregue":
                return {
                    "estado": "erro",
                    "mensagem": "O único estado final permitido é 'entregue'.",
                    "dados": {},
                }
            sucesso = Atualizar_estado_entrega(
                conexao, cursor, id_pedido, id_utilizador, estado
            )
            mensagem = (
                "Entrega marcada como concluída."
                if sucesso
                else "Não foi possível atualizar esta entrega."
            )

        return {
            "estado": "sucesso" if sucesso else "erro",
            "mensagem": mensagem,
            "dados": {"id_pedido": id_pedido} if sucesso else {},
        }

    return {
        "estado": "erro",
        "mensagem": "Operação desconhecida.",
        "dados": {},
    }

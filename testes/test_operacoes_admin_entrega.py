from decimal import Decimal
import unittest
from unittest.mock import patch

from server.base_de_dados import Aceitar_entrega, Adicionar_produto
from server.operacoes_admin_entrega import processar_operacao_admin_entrega
from server import socket_server

class CursorSimples:
    def __init__(self, resultados):
        self.resultados = iter(resultados)
        self.consultas = []

    def execute(self, consulta, parametros=None):
        self.consultas.append((consulta, parametros))

    def fetchone(self):
        return next(self.resultados)

class CursorAtualizacao:
    def __init__(self, rowcount):
        self.rowcount = rowcount
        self.consulta = ""
        self.parametros = None

    def execute(self, consulta, parametros):
        self.consulta = consulta
        self.parametros = parametros

class CursorInsercao:
    def __init__(self, lastrowid):
        self.lastrowid = lastrowid
        self.consulta = ""
        self.parametros = None

    def execute(self, consulta, parametros):
        self.consulta = consulta
        self.parametros = parametros

class ConexaoSimples:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

class CursorRota:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

class ConexaoRota:
    def __init__(self):
        self.cursor_obj = CursorRota()
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def close(self):
        self.closed = True

class TestOperacoesAdminEntrega(unittest.TestCase):
    def setUp(self):
        self.conexao = object()

    def test_admin_atualiza_stock(self):
        cursor = CursorSimples([(1,), (2,)])

        with patch(
            "server.operacoes_admin_entrega.Atualizar_stock",
            return_value=True,
        ) as atualizar_stock:
            resposta = processar_operacao_admin_entrega(
                "gerir_stock",
                {"id_utilizador": 9, "id_produto": 2, "stock": 15},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "sucesso")
        self.assertEqual(resposta["dados"]["stock"], 15)
        atualizar_stock.assert_called_once_with(self.conexao, cursor, 2, 15)

    def test_utilizador_nao_admin_nao_atualiza_stock(self):
        cursor = CursorSimples([None])

        with patch(
            "server.operacoes_admin_entrega.Atualizar_stock"
        ) as atualizar_stock:
            resposta = processar_operacao_admin_entrega(
                "gerir_stock",
                {"id_utilizador": 9, "id_produto": 2, "stock": 15},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "erro")
        atualizar_stock.assert_not_called()

    def test_admin_adiciona_produto(self):
        cursor = CursorSimples([(9,)])

        with patch(
            "server.operacoes_admin_entrega.Adicionar_produto",
            return_value=12,
        ) as adicionar:
            resposta = processar_operacao_admin_entrega(
                "adicionar_produto",
                {
                    "id_utilizador": 9,
                    "nome": "  Sumo  ",
                    "descricao": "  Natural  ",
                    "categoria": "  Bebidas  ",
                    "preco": "2.50",
                    "stock": 10,
                },
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "sucesso")
        self.assertEqual(resposta["dados"]["id_produto"], 12)
        chamada = adicionar.call_args.args
        self.assertEqual(chamada[:4], (self.conexao, cursor, "Sumo", "Natural"))
        self.assertEqual(chamada[4:], ("Bebidas", Decimal("2.50"), 10))

    def test_pedido_adicionar_produto_e_encaminhado_pelo_servidor(self):
        conexao = ConexaoRota()
        resposta_esperada = {
            "estado": "sucesso",
            "mensagem": "Produto adicionado com sucesso.",
            "dados": {"id_produto": 12},
        }

        with patch.object(socket_server, "conectar_bd", return_value=conexao):
            with patch(
                "server.socket_server.processar_operacao_admin_entrega",
                return_value=resposta_esperada,
            ) as processar:
                resposta = socket_server.processar_pedido(
                    {
                        "operacao": "adicionar_produto",
                        "dados": {"id_utilizador": 9, "nome": "Sumo"},
                    }
                )

        self.assertEqual(resposta, resposta_esperada)
        processar.assert_called_once_with(
            "adicionar_produto",
            {"id_utilizador": 9, "nome": "Sumo"},
            conexao,
            conexao.cursor_obj,
        )
        self.assertTrue(conexao.cursor_obj.closed)
        self.assertTrue(conexao.closed)

    def test_persistencia_de_produto_usa_insert_e_commit(self):
        conexao = ConexaoSimples()
        cursor = CursorInsercao(lastrowid=12)

        id_produto = Adicionar_produto(
            conexao,
            cursor,
            "Sumo",
            "Natural",
            "Bebidas",
            Decimal("2.50"),
            10,
        )

        self.assertEqual(id_produto, 12)
        self.assertIn("INSERT INTO produtos", cursor.consulta)
        self.assertEqual(
            cursor.parametros,
            ("Sumo", "Natural", "Bebidas", Decimal("2.50"), 10),
        )
        self.assertEqual(conexao.commits, 1)

    def test_utilizador_nao_admin_nao_adiciona_produto(self):
        cursor = CursorSimples([None])

        with patch(
            "server.operacoes_admin_entrega.Adicionar_produto"
        ) as adicionar:
            resposta = processar_operacao_admin_entrega(
                "adicionar_produto",
                {
                    "id_utilizador": 9,
                    "nome": "Sumo",
                    "descricao": "",
                    "categoria": "Bebidas",
                    "preco": "2.50",
                    "stock": 10,
                },
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "erro")
        adicionar.assert_not_called()

    def test_adicionar_produto_rejeita_preco_com_mais_de_duas_casas(self):
        cursor = CursorSimples([(9,)])

        with patch(
            "server.operacoes_admin_entrega.Adicionar_produto"
        ) as adicionar:
            resposta = processar_operacao_admin_entrega(
                "adicionar_produto",
                {
                    "id_utilizador": 9,
                    "nome": "Sumo",
                    "descricao": "",
                    "categoria": "Bebidas",
                    "preco": "2.555",
                    "stock": 10,
                },
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "erro")
        adicionar.assert_not_called()

    def test_admin_consulta_todos_os_pedidos(self):
        cursor = CursorSimples([(9,)])
        pedido = (4, 2, "cliente", "2026-10-27", "pendente", 12.5)

        with patch(
            "server.operacoes_admin_entrega.Consultar_pedidos",
            return_value=[pedido],
        ):
            resposta = processar_operacao_admin_entrega(
                "consultar_pedidos",
                {"id_utilizador": 9},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "sucesso")
        self.assertEqual(resposta["dados"]["pedidos"], [list(pedido)])

    def test_entregador_aceita_pedido_pendente(self):
        cursor = CursorSimples([(7,)])

        with patch(
            "server.operacoes_admin_entrega.Aceitar_entrega",
            return_value=True,
        ) as aceitar:
            resposta = processar_operacao_admin_entrega(
                "aceitar_entrega",
                {"id_utilizador": 7, "id_pedido": 4},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "sucesso")
        aceitar.assert_called_once_with(self.conexao, cursor, 4, 7)

    def test_entregador_so_conclui_com_estado_entregue(self):
        cursor = CursorSimples([(7,)])

        with patch(
            "server.operacoes_admin_entrega.Atualizar_estado_entrega",
            return_value=True,
        ) as atualizar:
            resposta = processar_operacao_admin_entrega(
                "atualizar_estado_entrega",
                {"id_utilizador": 7, "id_pedido": 4, "estado": "entregue"},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "sucesso")
        atualizar.assert_called_once_with(
            self.conexao, cursor, 4, 7, "entregue"
        )

    def test_rejeita_estado_final_invalido(self):
        cursor = CursorSimples([(7,)])

        with patch(
            "server.operacoes_admin_entrega.Atualizar_estado_entrega"
        ) as atualizar:
            resposta = processar_operacao_admin_entrega(
                "atualizar_estado_entrega",
                {"id_utilizador": 7, "id_pedido": 4, "estado": "cancelado"},
                self.conexao,
                cursor,
            )

        self.assertEqual(resposta["estado"], "erro")
        atualizar.assert_not_called()

    def test_aceitar_entrega_so_atualiza_pedido_pendente_nao_atribuido(self):
        conexao = ConexaoSimples()
        cursor = CursorAtualizacao(rowcount=1)

        self.assertTrue(Aceitar_entrega(conexao, cursor, 4, 7))
        self.assertIn("estado = 'pendente'", cursor.consulta)
        self.assertIn("id_entregador IS NULL", cursor.consulta)
        self.assertEqual(cursor.parametros, (7, 4))
        self.assertEqual(conexao.commits, 1)

    def test_pedido_ja_aceite_nao_e_reatribuido(self):
        conexao = ConexaoSimples()
        cursor = CursorAtualizacao(rowcount=0)

        self.assertFalse(Aceitar_entrega(conexao, cursor, 4, 8))
        self.assertEqual(conexao.commits, 0)
        self.assertEqual(conexao.rollbacks, 1)


if __name__ == "__main__":
    unittest.main()

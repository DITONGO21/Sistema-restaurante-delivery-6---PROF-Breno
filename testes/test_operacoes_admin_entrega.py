import unittest
from unittest.mock import patch

from server.base_de_dados import Aceitar_entrega
from server.operacoes_admin_entrega import processar_operacao_admin_entrega


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


class ConexaoSimples:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


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

import unittest

from cliente.menus import normalizar_tipo_utilizador
from server.base_de_dados import validar_estado_pedido


class TestFluxoSessao(unittest.TestCase):
    def test_normalizar_tipo_utilizador(self):
        self.assertEqual(normalizar_tipo_utilizador("Cliente"), "cliente")
        self.assertEqual(normalizar_tipo_utilizador("ADMIN"), "admin")
        self.assertEqual(normalizar_tipo_utilizador("entregador"), "entregador")

    def test_validar_estado_pedido(self):
        self.assertTrue(validar_estado_pedido("pendente"))
        self.assertTrue(validar_estado_pedido("em entrega"))
        self.assertFalse(validar_estado_pedido("estado_invalido"))


if __name__ == "__main__":
    unittest.main()

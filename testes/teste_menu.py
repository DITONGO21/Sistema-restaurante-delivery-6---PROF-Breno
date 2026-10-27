import unittest

from comum.validadores import campo_obrigatorio, validar_preco, validar_quantidade


class TesteMenu(unittest.TestCase):

    def test_campo_obrigatorio(self):
        self.assertTrue(campo_obrigatorio("Hamburguer"))
        self.assertFalse(campo_obrigatorio(""))
        self.assertFalse(campo_obrigatorio(None))

    def test_validar_preco(self):
        self.assertTrue(validar_preco(5.50))
        self.assertTrue(validar_preco(0))
        self.assertFalse(validar_preco(-2))
        self.assertFalse(validar_preco("abc"))

    def test_validar_quantidade(self):
        self.assertTrue(validar_quantidade(3))
        self.assertFalse(validar_quantidade(0))
        self.assertFalse(validar_quantidade(-1))
        self.assertFalse(validar_quantidade(2.5))


if __name__ == "__main__":
    unittest.main()
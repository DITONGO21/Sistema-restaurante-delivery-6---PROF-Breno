import unittest

def calcular_total(itens):
    total = 0
  
    for item in itens:
        preco = item["preco"]
        quantidade = item["quantidade"]
        total += preco * quantidade

    return round(total, 2)

class TesteOrders(unittest.TestCase):
    def test_calcular_total(self):
        itens = [
            {"preco": 5.00, "quantidade": 2},
            {"preco": 3.50, "quantidade": 1}
        ]
        self.assertEqual(calcular_total(itens), 13.50)
      
    def test_pedido_vazio(self):
        self.assertEqual(calcular_total([]), 0)

    def test_varios_produtos(self):
        itens = [
            {"preco": 10.00, "quantidade": 3},
            {"preco": 2.50, "quantidade": 4}
        ]
        self.assertEqual(calcular_total(itens), 40.00)

if __name__ == "__main__":
    unittest.main()

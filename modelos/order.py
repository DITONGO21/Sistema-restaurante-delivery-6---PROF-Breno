from datetime import datetime

class Order:
    def __init__(self, id_pedido, id_cliente):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.itens = []
        self.status = "em preparação"
        self.data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.total = 0

    def adicionar_item(self, id_produto, nome, preco, quantidade):
        item = {
            "id_produto": id_produto,
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade
        }
        self.itens.append(item)
        self.total = self.total + (preco * quantidade)

    def atualizar_status(self, novo_status):
        self.status = novo_status

    def apresentar_dados(self):
        return {
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "itens": self.itens,
            "total": self.total,
            "status": self.status,
            "data": self.data
        }
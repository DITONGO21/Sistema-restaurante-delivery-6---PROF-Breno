class Produto:
    def __init__(self, id_produto, nome, descricao, categoria, preco, stock):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.preco = preco
        self.stock = stock

    def atualizar_preco(self, novo_preco):
        if novo_preco < 0:
            return False

        self.preco = novo_preco
        return True

    def atualizar_stock(self, quantidade):
        if self.stock + quantidade < 0:
            return False

        self.stock += quantidade
        return True

    def verificar_disponibilidade(self, quantidade=1):
        return quantidade > 0 and self.stock >= quantidade

    def apresentar_dados(self):
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "preco": self.preco,
            "stock": self.stock
        }

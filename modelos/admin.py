from modelos.usuario import Usuario

class Admin(Usuario):
    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "admin")

    def gerir_produtos(self):
        return {"estado": "ok", "mensagem": "Produtos geridos."}

    def gerir_utilizadores(self):
        return {"estado": "ok", "mensagem": "Utilizadores geridos."}

    def consultar_pedidos(self):
        return {"estado": "ok", "mensagem": "Pedidos consultados."}

    def gerir_stock(self):
        return {"estado": "ok", "mensagem": "Stock atualizado."}

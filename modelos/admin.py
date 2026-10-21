from modelos.usuario import Usuario

class Admin(Usuario):

    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "admin")

    def gerir_produtos(self):
        pass

    def gerir_utilizadores(self):
        pass

    def consultar_pedidos(self):
        pass

    def gerir_stock(self):
        pass
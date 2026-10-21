from modelos.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "cliente")

    def mostrar_menu(self):
        pass

    def consultar_menu(self):
        pass

    def criar_pedido(self):
        pass

    def consultar_historico(self):
        pass
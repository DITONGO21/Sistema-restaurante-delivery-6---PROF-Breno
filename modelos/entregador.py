from modelos.usuario import Usuario

class Entregador(Usuario):
    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "entregador")

    def consultar_entregas(self):
        pass

    def aceitar_entrega(self, id_pedido):
        pass

    def atualizar_estado_entrega(self, id_pedido, novo_estado):
        pass
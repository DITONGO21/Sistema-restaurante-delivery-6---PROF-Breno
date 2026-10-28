from modelos.usuario import Usuario

class Entregador(Usuario):
    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "entregador")

    def consultar_entregas(self):
        return {"estado": "ok", "mensagem": "Entregas consultadas."}

    def aceitar_entrega(self, id_pedido):
        return {"estado": "ok", "mensagem": f"Entrega {id_pedido} aceite."}

    def atualizar_estado_entrega(self, id_pedido, novo_estado):
        return {"estado": "ok", "mensagem": f"Entrega {id_pedido} alterada para {novo_estado}."}

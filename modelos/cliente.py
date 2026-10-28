from modelos.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, id_utilizador, nome_utilizador, password_hash):
        super().__init__(id_utilizador, nome_utilizador, password_hash, "cliente")

    def mostrar_menu(self):
        return {
            "tipo": "cliente",
            "opcoes": ["ver_produtos", "criar_pedido", "historico"],
        }
    def consultar_menu(self):
        return self.mostrar_menu()

    def criar_pedido(self):
        return {"estado": "ok", "mensagem": "Pedido em preparação."}

    def consultar_historico(self):
        return {"estado": "ok", "mensagem": "Histórico consultado."}

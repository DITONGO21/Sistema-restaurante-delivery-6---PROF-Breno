from usuario import Usuario

class Cliente:
    def __init__(self, monstrar_menu, consultar_menu, criar_pedido, consultar_historico):
        self.monstrar_menu = monstrar_menu
        self.consultar_menu = consultar_menu
        self.criar_pedido = criar_pedido
        self.consultar_historico = consultar_historico

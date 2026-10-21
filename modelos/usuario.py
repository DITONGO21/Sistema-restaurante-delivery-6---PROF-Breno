class Usuario:
    def __init__(self, id_utilizador, nome_utilizador, password_hash, tipo_utilizador):
        self.id_utilizador = id_utilizador
        self.nome_utilizador = nome_utilizador
        self.password_hash = password_hash
        self.tipo_utilizador = tipo_utilizador

    def apresentar_dados(self):
        return {
            "id": self.id_utilizador,
            "nome": self.nome_utilizador,
            "tipo": self.tipo_utilizador
        }

    def mostrar_menu(self):
        print("Menu de utilizador")

    def verificar_tipo(self, tipo):
        return self.tipo_utilizador == tipo

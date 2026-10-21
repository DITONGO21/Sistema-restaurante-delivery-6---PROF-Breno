
import mysql.connector


def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurante_delivery",
            connect_timeout=10
        )

        if conexao.is_connected():
            print("Ligação ao MySQL estabelecida!")
            return conexao

    except mysql.connector.Error as erro:
        print(f"Erro ao ligar ao MySQL: {erro}")

    return None


if __name__ == "__main__":
    conexao = conectar_bd()

    if conexao is not None:
        conexao.close()

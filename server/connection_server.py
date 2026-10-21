import mysql.connector
import psycopg2
from psycopg2 import OperationalError, DatabaseError

def conectar_bd():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurante_delivery",
            connect_timeout=10
        )
        return conexao
    except OperationalError as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

    except DatabaseError as e:
        print(f"Erro de banco de dados: {e}")
        return None

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

conexao = conectar_bd()

if conexao.is_connected():
    print("Ligação ao MySQL estabelecida")
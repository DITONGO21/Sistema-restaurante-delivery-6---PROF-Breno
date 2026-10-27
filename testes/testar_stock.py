from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from server.connection_server import conectar_bd
from server.base_de_dados import Atualizar_stock

conexao = conectar_bd()

if conexao is None:
    print("Não foi possível ligar à base de dados.")
    sys.exit()

cursor = conexao.cursor()

try:
    id_produto = int(input("ID do produto a testar: "))

    # Consultar o stock atual
    cursor.execute(
        "SELECT nome, stock FROM produtos WHERE id_produto = %s",
        (id_produto,)
    )
    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado.")
        sys.exit()

    nome, stock_original = produto

    print(f"\nProduto: {nome}")
    print(f"Stock atual: {stock_original}")

    # Testar a atualização do stock
    nova_quantidade = int(input("Novo stock: "))

    resultado = Atualizar_stock(
        conexao,
        cursor,
        id_produto,
        nova_quantidade
    )

    if resultado:
        print("Stock atualizado com sucesso!")
    else:
        print("Não foi possível atualizar o stock.")

    # Confirmar o stock na base de dados
    cursor.execute(
        "SELECT stock FROM produtos WHERE id_produto = %s",
        (id_produto,)
    )
    resultado_stock = cursor.fetchone()

    if resultado_stock:
        print("Stock final:", resultado_stock[0])

finally:
    cursor.close()
    conexao.close()

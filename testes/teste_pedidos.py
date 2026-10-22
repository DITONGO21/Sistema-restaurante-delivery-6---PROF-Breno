from server.connection_server import conectar_bd
from server.base_de_dados import Consultar_produtos

mybd = conectar_bd()
mycursor = mybd.cursor()

try:
    print("A testar consulta de produtos...\n")

    # Consultar todos os produtos
    produtos = Consultar_produtos(mycursor, "")

    if produtos:
        print("Produtos encontrados:\n")

        for produto in produtos:
            print("-----------------------------")
            print(f"ID: {produto[0]}")
            print(f"Nome: {produto[1]}")
            print(f"Descrição: {produto[2]}")
            print(f"Categoria: {produto[3]}")
            print(f"Preço: {produto[4]} €")
            print(f"Stock: {produto[5]}")

        print("\nTeste concluído!")
    else:
        print("Não foram encontrados produtos.")

finally:
    mycursor.close()
    mybd.close()
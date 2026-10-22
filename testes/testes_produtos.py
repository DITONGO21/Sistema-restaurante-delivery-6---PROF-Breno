from server.connection_server import conectar_bd

mybd = conectar_bd()
mycursor = mybd.cursor()

try:
    mycursor.execute("SELECT * FROM produtos")
    produtos = mycursor.fetchall()

    print("\nProdutos encontrados diretamente no MySQL:")

    for produto in produtos:
        print(produto)

    print(f"\nTotal de produtos: {len(produtos)}")

finally:
    mycursor.close()
    mybd.close()
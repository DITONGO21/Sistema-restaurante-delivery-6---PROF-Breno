from cliente.connection_clientes import enviar_pedido

id_cliente = 1
id_produto = 1

resposta = enviar_pedido(
    "criar_pedido",
    {
        "id_utilizador": id_cliente,
        "id_produto": id_produto,
        "quantidade": 1
    }
)

print("Resposta:", resposta)

if resposta["estado"] == "erro":
    print("Teste passou: o pedido acima do stock foi rejeitado.")
else:
    print("ATENÇÃO: o servidor aceitou o pedido.")

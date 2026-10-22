
from cliente.connection_clientes import enviar_pedido

resposta = enviar_pedido(
    "historico_pedidos",
    {"id_utilizador": 3}
)

print("Resposta:", resposta)

if resposta["estado"] == "sucesso":
    pedidos = resposta["dados"]["pedidos"]

    if pedidos:
        for pedido in pedidos:
            print("Pedido:", pedido)
    else:
        print("Este cliente ainda não tem pedidos.")
else:
    print("Erro:", resposta["mensagem"])

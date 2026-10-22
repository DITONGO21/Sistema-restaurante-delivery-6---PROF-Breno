
from cliente.connection_clientes import enviar_pedido

resposta = enviar_pedido(
    "historico_pedidos",
    {"id_utilizador": 999999}
)

print("Resposta:", resposta)

if resposta["estado"] == "erro":
    print("Teste passou: cliente inexistente rejeitado.")
else:
    print("ATENÇÃO: o servidor aceitou o pedido.")

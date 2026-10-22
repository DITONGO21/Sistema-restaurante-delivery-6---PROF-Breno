
from cliente.connection_clientes import enviar_pedido

resposta = enviar_pedido("listar_produtos", {"nome": "Pizza"})

print("Resposta:", resposta)

assert resposta["estado"] == "sucesso"
assert "produtos" in resposta["dados"]

produtos = resposta["dados"]["produtos"]

for produto in produtos:
    print(produto)

assert any(produto[1] == "Pizza" for produto in produtos)

print("Consulta de produtos por sockets passou!")

from cliente.connection_clientes import enviar_pedido

nome = "teste_socket_novo"
password = "Teste123!"

# Tentar registar o utilizador
registo = enviar_pedido(
    "registar",
    {
        "nome": nome,
        "password": password
    }
)

print("Registo:", registo)

# Testar o login
login = enviar_pedido(
    "login",
    {
        "nome": nome,
        "password": password
    }
)

print("Login:", login)

assert login["estado"] == "sucesso"
assert login["dados"]["nome_utilizador"] == nome
assert "password_hash" not in login["dados"]

print("Teste de login por sockets passou!")

import socket
import json

HOST = "127.0.0.1"
PORT = 5000

def enviar_pedido(operacao, dados=None):
    pedido = {
        "operacao": operacao,
        "dados": dados or {}
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect((HOST, PORT))
        cliente_socket.sendall(
            json.dumps(pedido, ensure_ascii=False).encode("utf-8")
            )

        resposta = cliente_socket.recv(1024)

    return json.loads(resposta.decode("utf-8"))
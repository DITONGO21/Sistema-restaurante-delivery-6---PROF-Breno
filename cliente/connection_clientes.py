
import json
import os
import socket

HOST = os.getenv("DELIVER_HOST", "127.0.0.1")
PORT = int(os.getenv("DELIVER_PORT", "5000"))


def enviar_pedido(operacao, dados=None):
    pedido = {
        "operacao": operacao,
        "dados": dados or {}
    }

    print("A enviar:", pedido)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
            cliente_socket.settimeout(10)
            cliente_socket.connect((HOST, PORT))

            cliente_socket.sendall(
                json.dumps(pedido, ensure_ascii=False).encode("utf-8")
            )

            resposta = cliente_socket.recv(4096)

        return json.loads(resposta.decode("utf-8"))

    except (OSError, ConnectionError, TimeoutError, json.JSONDecodeError):
        return {
            "estado": "erro",
            "mensagem": "Servidor indisponível. Inicia o servidor antes de continuar.",
            "dados": {}
        }

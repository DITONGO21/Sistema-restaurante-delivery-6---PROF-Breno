
import json
import socket

from server.connection_server import conectar_bd
from server.base_de_dados import (
    Consultar_produtos,
    Consultar_utilizador,
    Criar_pedidos,
    Consultar_historico_pedidos
)
from server.autenticação import (
    registar_utilizador,
    autenticar_utilizador
)

HOST = "127.0.0.1"
PORT = 5000


def processar_pedido(pedido):
    if not isinstance(pedido, dict):
        return {
            "estado": "erro",
            "mensagem": "Pedido inválido",
            "dados": {}
        }

    operacao = pedido.get("operacao")
    dados = pedido.get("dados", {})

    if not isinstance(dados, dict):
        return {
            "estado": "erro",
            "mensagem": "Dados inválidos",
            "dados": {}
        }

    # LISTAR PRODUTOS
    if operacao == "listar_produtos":
        conexao = conectar_bd()

        if conexao is None:
            return {
                "estado": "erro",
                "mensagem": "Não foi possível ligar à base de dados",
                "dados": {}
            }

        cursor = None

        try:
            cursor = conexao.cursor()
            nome = dados.get("nome", "")

            if not isinstance(nome, str):
                return {
                    "estado": "erro",
                    "mensagem": "O nome tem de ser texto",
                    "dados": {}
                }

            produtos = Consultar_produtos(cursor, nome)

            return {
                "estado": "sucesso",
                "mensagem": "Produtos consultados",
                "dados": {
                    "produtos": [list(produto) for produto in produtos]
                }
            }

        except Exception as erro:
            print(f"Erro ao consultar produtos: {erro}")
            return {
                "estado": "erro",
                "mensagem": "Erro ao consultar produtos",
                "dados": {}
            }

        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    # REGISTAR E LOGIN
    if operacao in ("registar", "login"):
        nome = dados.get("nome")
        password = dados.get("password")

        if not isinstance(nome, str) or not nome.strip():
            return {
                "estado": "erro",
                "mensagem": "Nome inválido",
                "dados": {}
            }

        if not isinstance(password, str) or not password:
            return {
                "estado": "erro",
                "mensagem": "Palavra-passe inválida",
                "dados": {}
            }

        conexao = conectar_bd()

        if conexao is None:
            return {
                "estado": "erro",
                "mensagem": "Erro de ligação à base de dados",
                "dados": {}
            }

        cursor = None

        try:
            cursor = conexao.cursor()
            nome = nome.strip()

            if operacao == "registar":
                tipo = dados.get("tipo", "cliente")

                if tipo != "cliente":
                    return {
                        "estado": "erro",
                        "mensagem": "Só é permitido registar contas de cliente",
                        "dados": {}
                    }

                sucesso = registar_utilizador(
                    conexao,
                    cursor,
                    nome,
                    password,
                    "cliente"
                )

                if not sucesso:
                    return {
                        "estado": "erro",
                        "mensagem": "Não foi possível registar. O nome pode já existir.",
                        "dados": {}
                    }

                return {
                    "estado": "sucesso",
                    "mensagem": "Conta criada com sucesso",
                    "dados": {}
                }

            # LOGIN
            if autenticar_utilizador(cursor, nome, password):
                utilizador = Consultar_utilizador(cursor, nome)

                if utilizador is None:
                    return {
                        "estado": "erro",
                        "mensagem": "Não foi possível obter os dados do utilizador",
                        "dados": {}
                    }

                return {
                    "estado": "sucesso",
                    "mensagem": "Login efetuado",
                    "dados": {
                        "id_utilizador": utilizador[0],
                        "nome_utilizador": utilizador[1],
                        "tipo_utilizador": utilizador[3]
                    }
                }

            return {
                "estado": "erro",
                "mensagem": "Nome ou palavra-passe incorretos",
                "dados": {}
            }

        except Exception as erro:
            print(f"Erro na autenticação: {erro}")
            return {
                "estado": "erro",
                "mensagem": "Erro ao processar a autenticação",
                "dados": {}
            }

        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    # CRIAR PEDIDO
    if operacao == "criar_pedido":
        id_utilizador = dados.get("id_utilizador")
        id_produto = dados.get("id_produto")
        quantidade = dados.get("quantidade")

        if (
            not isinstance(id_utilizador, int)
            or isinstance(id_utilizador, bool)
            or id_utilizador <= 0
            or not isinstance(id_produto, int)
            or isinstance(id_produto, bool)
            or id_produto <= 0
            or not isinstance(quantidade, int)
            or isinstance(quantidade, bool)
            or quantidade <= 0
        ):
            return {
                "estado": "erro",
                "mensagem": "Dados do pedido inválidos",
                "dados": {}
            }

        conexao = conectar_bd()

        if conexao is None:
            return {
                "estado": "erro",
                "mensagem": "Erro de ligação à base de dados",
                "dados": {}
            }

        cursor = None

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT id_utilizador
                FROM utilizadores
                WHERE id_utilizador = %s
                AND tipo_utilizador = 'cliente'
                """,
                (id_utilizador,)
            )

            if cursor.fetchone() is None:
                return {
                    "estado": "erro",
                    "mensagem": "Cliente não encontrado",
                    "dados": {}
                }

            id_pedido = Criar_pedidos(
                conexao,
                cursor,
                id_utilizador,
                id_produto,
                quantidade
            )

            if not id_pedido:
                return {
                    "estado": "erro",
                    "mensagem": "Não foi possível criar o pedido. Verifica o produto e o stock.",
                    "dados": {}
                }

            return {
                "estado": "sucesso",
                "mensagem": "Pedido criado com sucesso",
                "dados": {
                    "id_pedido": id_pedido
                }
            }

        except Exception as erro:
            print(f"Erro ao criar pedido: {erro}")
            return {
                "estado": "erro",
                "mensagem": "Erro ao criar pedido",
                "dados": {}
            }

        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    # HISTÓRICO DE PEDIDOS
    if operacao == "historico_pedidos":
        id_utilizador = dados.get("id_utilizador")

        if (
            not isinstance(id_utilizador, int)
            or isinstance(id_utilizador, bool)
            or id_utilizador <= 0
        ):
            return {
                "estado": "erro",
                "mensagem": "ID do cliente inválido",
                "dados": {}
            }

        conexao = conectar_bd()

        if conexao is None:
            return {
                "estado": "erro",
                "mensagem": "Erro de ligação à base de dados",
                "dados": {}
            }

        cursor = None

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT id_utilizador
                FROM utilizadores
                WHERE id_utilizador = %s
                AND tipo_utilizador = 'cliente'
                """,
                (id_utilizador,)
            )

            if cursor.fetchone() is None:
                return {
                    "estado": "erro",
                    "mensagem": "Cliente não encontrado",
                    "dados": {}
                }

            pedidos = Consultar_historico_pedidos(
                cursor,
                id_utilizador
            )

            if pedidos is None:
                return {
                    "estado": "erro",
                    "mensagem": "Erro ao consultar o histórico",
                    "dados": {}
                }

            return {
                "estado": "sucesso",
                "mensagem": "Histórico consultado",
                "dados": {
                    "pedidos": [list(pedido) for pedido in pedidos]
                }
            }

        except Exception as erro:
            print(f"Erro ao consultar histórico: {erro}")
            return {
                "estado": "erro",
                "mensagem": "Erro ao consultar histórico",
                "dados": {}
            }

        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    # OPERAÇÃO DESCONHECIDA
    return {
        "estado": "erro",
        "mensagem": "Operação desconhecida",
        "dados": {}
    }


def iniciar_server():
    servidor_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor_socket.bind((HOST, PORT))
    servidor_socket.listen()

    print(f"Servidor está em: {HOST}:{PORT}")

    try:
        while True:
            cliente, endereco = servidor_socket.accept()

            with cliente:
                print(f"Cliente ligado: {endereco}")

                try:
                    dados = cliente.recv(4096)

                    if not dados:
                        continue

                    pedido = json.loads(
                        dados.decode("utf-8")
                    )

                    resposta = processar_pedido(pedido)

                except (
                    json.JSONDecodeError,
                    UnicodeDecodeError
                ):
                    resposta = {
                        "estado": "erro",
                        "mensagem": "Pedido inválido",
                        "dados": {}
                    }

                except Exception as erro:
                    print(f"Erro ao processar pedido: {erro}")
                    resposta = {
                        "estado": "erro",
                        "mensagem": "Erro interno do servidor",
                        "dados": {}
                    }

                cliente.sendall(
                    json.dumps(
                        resposta,
                        ensure_ascii=False,
                        default=str
                    ).encode("utf-8")
                )

    except KeyboardInterrupt:
        print("\nServidor encerrado.")

    finally:
        servidor_socket.close()


if __name__ == "__main__":
    iniciar_server()

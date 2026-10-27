import sys

def main():
    while True:
        print("\n==============================")
        print(" DELIVER RESTAURANT")
        print("==============================")
        print("1 - Iniciar servidor")
        print("2 - Iniciar cliente")
        print("0 - Sair")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            from server.main_server import main as iniciar_servidor

            iniciar_servidor()

        elif opcao == "2":
            from cliente.main_clientes import main as iniciar_cliente

            iniciar_cliente()

        elif opcao == "0":
            print("Programa terminado.")
            sys.exit(0)

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
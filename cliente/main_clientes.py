from cliente.menus import (
    mostrar_produtos,
    menu_registo,
    menu_login,
    menu_por_tipo
)


def main():
    while True:
        print("\n=== DELIVER RESTAURANT ===")
        print("1 - Ver produtos")
        print("2 - Criar conta")
        print("3 - Iniciar sessão")
        print("0 - Sair")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_produtos()

        elif opcao == "2":
            menu_registo()

        elif opcao == "3":
            utilizador = menu_login()

            if utilizador:
                menu_por_tipo(utilizador)

        elif opcao == "0":
            print("Até à próxima!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
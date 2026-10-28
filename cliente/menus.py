from cliente.operations_clientes import (
    listar_produtos,
    registar_utilizador,
    login_utilizador,
    criar_pedido,
    consultar_historico,
    adicionar_produto,
    gerir_stock,
    consultar_pedidos,
    consultar_entregas,
    aceitar_entrega,
    concluir_entrega,
)

TIPOS_UTILIZADOR = {
    "1": "cliente",
    "2": "entregador",
    "3": "admin",
}

def normalizar_tipo_utilizador(tipo):
    if tipo is None:
        return "cliente"

    texto = str(tipo).strip().lower()
    if texto in {"cliente", "1"}:
        return "cliente"
    if texto in {"entregador", "2"}:
        return "entregador"
    if texto in {"admin", "3"}:
        return "admin"
    return "cliente"

def mostrar_produtos():
    nome = input("Nome do produto (Enter para todos): ").strip()
    resposta = listar_produtos(nome)

    print("\n--- PRODUTOS ---")

    if resposta.get("estado") != "sucesso":
        print(resposta.get("mensagem", "Erro ao consultar produtos."))
        return

    produtos = resposta.get("dados", {}).get("produtos", [])

    if not produtos:
        print("Não existem produtos.")
        return

    for produto in produtos:
        print(
            f"ID: {produto[0]} | "
            f"Nome: {produto[1]} | "
            f"Preço: {produto[4]} € | "
            f"Stock: {produto[5]}"
        )

def menu_registo():
    nome = input("Nome de utilizador: ").strip()
    password = input("Palavra-passe: ")

    print("Tipo de utilizador:")
    print("1 - Cliente")
    print("2 - Entregador")
    print("3 - Admin")
    tipo_input = input("Escolha uma opção: ").strip()
    tipo = TIPOS_UTILIZADOR.get(tipo_input, "cliente")

    resposta = registar_utilizador(nome, password, tipo)
    print(resposta.get("mensagem", "Sem resposta do servidor."))
    return resposta

def menu_login():
    nome = input("Nome de utilizador: ").strip()
    password = input("Palavra-passe: ")

    resposta = login_utilizador(nome, password)

    print(resposta.get("mensagem", "Sem resposta do servidor."))

    if resposta.get("estado") == "sucesso":
        dados = resposta.get("dados", {})
        dados["tipo_utilizador"] = dados.get("tipo_utilizador", "cliente")
        return dados

    return None

def menu_criar_pedido(utilizador):
    try:
        id_produto = int(input("ID do produto: "))
        quantidade = int(input("Quantidade: "))

        resposta = criar_pedido(
            utilizador["id_utilizador"],
            id_produto,
            quantidade
        )

        print(resposta.get("mensagem", "Sem resposta do servidor."))

        if resposta.get("estado") == "sucesso":
            print("ID do pedido:", resposta["dados"]["id_pedido"])

    except ValueError:
        print("Introduz números inteiros válidos.")

def menu_historico(utilizador):
    resposta = consultar_historico(utilizador["id_utilizador"])

    print("\n--- HISTÓRICO DE PEDIDOS ---")

    if resposta.get("estado") != "sucesso":
        print(resposta.get("mensagem", "Erro ao consultar histórico."))
        return

    pedidos = resposta.get("dados", {}).get("pedidos", [])

    if not pedidos:
        print("Ainda não tens pedidos.")
        return

    for pedido in pedidos:
        estado = pedido[3] if len(pedido) > 3 else "desconhecido"
        print(f"Pedido: {pedido[0]} | Estado: {estado} | Total: {pedido[4] if len(pedido) > 4 else 'N/A'}")

def menu_entregas(utilizador):
    resposta = consultar_entregas(utilizador["id_utilizador"])
    print("\n--- ENTREGAS ---")

    if resposta.get("estado") != "sucesso":
        print(resposta.get("mensagem", "Erro ao consultar entregas."))
        return

    entregas = resposta.get("dados", {}).get("entregas", [])
    if not entregas:
        print("Não existem entregas disponíveis ou atribuídas.")
        return

    for entrega in entregas:
        id_entregador = entrega[5] if len(entrega) > 5 else None
        atribuicao = (
            "atribuída a ti"
            if id_entregador == utilizador["id_utilizador"]
            else "disponível"
        )
        print(
            f"Pedido: {entrega[0]} | Cliente: {entrega[1]} | "
            f"Estado: {entrega[3]} | Total: {entrega[4]} € | {atribuicao}"
        )

def menu_gerir_stock(utilizador):
    try:
        id_produto = int(input("ID do produto: "))
        stock = int(input("Novo stock: "))
    except ValueError:
        print("Introduz números inteiros válidos.")
        return

    resposta = gerir_stock(utilizador["id_utilizador"], id_produto, stock)
    print(resposta.get("mensagem", "Sem resposta do servidor."))

def menu_adicionar_produto(utilizador):
    from decimal import Decimal, InvalidOperation

    nome = input("Nome do produto: ").strip()
    descricao = input("Descrição (opcional): ").strip()
    categoria = input("Categoria: ").strip()

    try:
        preco = Decimal(input("Preço (€): ").strip().replace(",", "."))
        stock = int(input("Stock inicial: ").strip())
    except (InvalidOperation, ValueError):
        print("Introduz um preço e um stock válidos.")
        return

    if not preco.is_finite():
        print("Introduz um preço válido.")
        return

    resposta = adicionar_produto(
        utilizador["id_utilizador"],
        nome,
        descricao,
        categoria,
        str(preco),
        stock,
    )
    print(resposta.get("mensagem", "Sem resposta do servidor."))
    if resposta.get("estado") == "sucesso":
        print("ID do produto:", resposta.get("dados", {}).get("id_produto"))

def menu_consultar_pedidos(utilizador):
    resposta = consultar_pedidos(utilizador["id_utilizador"])
    print("\n--- TODOS OS PEDIDOS ---")

    if resposta.get("estado") != "sucesso":
        print(resposta.get("mensagem", "Erro ao consultar pedidos."))
        return

    pedidos = resposta.get("dados", {}).get("pedidos", [])
    if not pedidos:
        print("Ainda não existem pedidos.")
        return

    for pedido in pedidos:
        print(
            f"Pedido: {pedido[0]} | Cliente: {pedido[2]} (ID: {pedido[1]}) | "
            f"Data: {pedido[3]} | Estado: {pedido[4]} | Total: {pedido[5]} €"
        )

def menu_cliente(utilizador):
    while True:
        print(f"\n=== MENU DO CLIENTE - {utilizador.get('nome_utilizador', 'Utilizador')} ===")
        print("1 - Ver produtos")
        print("2 - Criar pedido")
        print("3 - Consultar histórico")
        print("0 - Terminar sessão")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_produtos()
        elif opcao == "2":
            menu_criar_pedido(utilizador)
        elif opcao == "3":
            menu_historico(utilizador)
        elif opcao == "0":
            print("Sessão terminada.")
            break
        else:
            print("Opção inválida.")

def menu_entregador(utilizador):
    while True:
        print(f"\n=== MENU DO ENTREGADOR - {utilizador.get('nome_utilizador', 'Utilizador')} ===")
        print("1 - Ver produtos")
        print("2 - Ver entregas")
        print("3 - Aceitar entrega")
        print("4 - Marcar entrega como concluída")
        print("0 - Terminar sessão")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_produtos()
        elif opcao == "2":
            menu_entregas(utilizador)
        elif opcao == "3":
            try:
                id_pedido = int(input("ID do pedido a aceitar: "))
                resposta = aceitar_entrega(
                    utilizador["id_utilizador"], id_pedido
                )
                print(resposta.get("mensagem", "Sem resposta do servidor."))
            except ValueError:
                print("Introduz um ID de pedido válido.")
        elif opcao == "4":
            try:
                id_pedido = int(input("ID do pedido concluído: "))
                resposta = concluir_entrega(
                    utilizador["id_utilizador"], id_pedido
                )
                print(resposta.get("mensagem", "Sem resposta do servidor."))
            except ValueError:
                print("Introduz um ID de pedido válido.")
        elif opcao == "0":
            print("Sessão terminada.")
            break
        else:
            print("Opção inválida.")

def menu_admin(utilizador):
    while True:
        print(f"\n=== MENU DO ADMIN - {utilizador.get('nome_utilizador', 'Utilizador')} ===")
        print("1 - Ver produtos")
        print("2 - Gerir stock")
        print("3 - Ver pedidos")
        print("4 - Adicionar produto")
        print("0 - Terminar sessão")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            mostrar_produtos()
        elif opcao == "2":
            menu_gerir_stock(utilizador)
        elif opcao == "3":
            menu_consultar_pedidos(utilizador)
        elif opcao == "4":
            menu_adicionar_produto(utilizador)
        elif opcao == "0":
            print("Sessão terminada.")
            break
        else:
            print("Opção inválida.")

def menu_por_tipo(utilizador):
    tipo = normalizar_tipo_utilizador(utilizador.get("tipo_utilizador") if isinstance(utilizador, dict) else utilizador)

    if tipo == "cliente":
        menu_cliente(utilizador)
    elif tipo == "entregador":
        menu_entregador(utilizador)
    elif tipo == "admin":
        menu_admin(utilizador)
    else:
        menu_cliente(utilizador)

from comum.protocologo import criar_mensagem, ler_mensagem, criar_resposta

mensagem = criar_mensagem("listar_produtos", {"nome": "Pizza"})
resultado = ler_mensagem(mensagem)

assert resultado is not None
assert resultado["operacao"] == "listar_produtos"
assert resultado["dados"]["nome"] == "Pizza"

resposta = criar_resposta("sucesso", "Produtos encontrados", [])
print("Mensagem:", mensagem)
print("Resposta:", resposta)
print("Testes do protocolo passaram!")

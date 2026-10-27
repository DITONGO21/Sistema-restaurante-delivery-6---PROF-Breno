from comum.validadores import (
    campo_obrigatorio,
    validar_quantidade,
    validar_preco,
    validar_stock,
    validar_produto
)

assert campo_obrigatorio("Hamburguer")
assert not campo_obrigatorio("   ")

assert validar_quantidade(2)
assert not validar_quantidade(0)
assert not validar_quantidade(-1)

assert validar_preco(8.50)
assert not validar_preco(float("nan"))
assert not validar_preco(float("inf"))
assert not validar_preco(-1)

assert validar_stock(0)
assert validar_stock(10)
assert not validar_stock(-1)

assert validar_produto("Pizza", 10.0, 5)
assert validar_produto("Pizza", 10.0, 0)
assert not validar_produto("", 10.0, 5)

print("Todos os testes dos validadores passaram!")

# Deliver Restaurant

Aplicação de pedidos de restaurante em Python. O cliente comunica com um
servidor TCP, que valida as operações e guarda os dados numa base de dados
MySQL.

## Requisitos

- Python 3.10 ou superior
- MySQL Server
- Pacotes Python `mysql-connector-python` e `bcrypt`

Instala os pacotes necessários:

```powershell
python -m pip install -r requirements.txt
```

## Configuração da base de dados

Por omissão, a aplicação liga ao MySQL local com o utilizador `root`, sem
palavra-passe, e usa a base de dados `restaurante_delivery`. Se necessário,
altera as credenciais em `server/connection_server.py` e `base_de_dados/esquema.py`
para corresponder à tua instalação MySQL.

Cria as tabelas e atualiza uma base de dados existente com a coluna usada para
atribuir pedidos a entregadores:

```powershell
python base_de_dados\esquema.py
```

Executa este passo antes de iniciar o servidor pela primeira vez e sempre que
instalares uma versão que altere o esquema da base de dados.

## Iniciar a aplicação

Na pasta do projeto, executa:

```powershell
python main.py
```

No menu inicial:

1. Escolhe `1 - Iniciar servidor` para iniciar o servidor.
2. Abre uma segunda janela de terminal na pasta do projeto e executa
   `python main.py`.
3. Na segunda janela, escolhe `2 - Iniciar cliente`.

O cliente usa `127.0.0.1:5000` por omissão. Para ligar a um servidor noutro
computador, define as variáveis de ambiente `DELIVER_HOST` e `DELIVER_PORT` no
terminal do cliente. O servidor escuta na porta `5000`.

## Funcionalidades

### Cliente

- Consultar e filtrar produtos pelo nome.
- Criar uma conta de cliente e iniciar sessão.
- Criar pedidos, com validação de stock e atualização da quantidade disponível.
- Consultar o histórico e o estado dos seus pedidos.

### Entregador

- Consultar pedidos pendentes e entregas que aceitou.
- Aceitar um pedido pendente; cada pedido só pode ser atribuído a um entregador.
- Marcar como entregue um pedido que lhe esteja atribuído.

### Administrador

- Consultar todos os pedidos.
- Atualizar o stock de um produto.
- Adicionar produtos com nome, descrição opcional, categoria, preço e stock inicial.

## Testes

Executa os testes automatizados com:

```powershell
python -m unittest discover -s testes -p "test_*.py"
```

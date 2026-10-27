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

O MySQL e a base de dados devem estar no computador que executa o servidor.
O cliente não precisa de instalar MySQL nem de se ligar diretamente à base de
dados.

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

## Executar em dois computadores Windows na mesma rede

Liga ambos os computadores à mesma rede local (por exemplo, ao mesmo router).
O servidor e o cliente comunicam por TCP na porta `5000`.

### No computador servidor

1. Instala Python, MySQL Server e as dependências do projeto:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Configura as credenciais MySQL nos ficheiros indicados acima e prepara a
   base de dados:

   ```powershell
   python base_de_dados\esquema.py
   ```

3. Abre o Windows Defender Firewall para permitir ligações TCP de entrada na
   porta `5000` em redes privadas. Num PowerShell executado como administrador,
   podes criar uma regra limitada à rede local:

   ```powershell
   New-NetFirewallRule -DisplayName "Deliver Restaurant" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow -Profile Private -RemoteAddress LocalSubnet
   ```

4. Descobre o IPv4 do servidor com `ipconfig` (por exemplo,
   `192.168.1.117`).
5. Inicia o servidor:

   ```powershell
   python main.py
   ```

   Escolhe `1 - Iniciar servidor` e deixa esta janela aberta.

### No computador cliente

1. Instala Python e as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Na pasta do projeto, define o IPv4 do computador servidor e inicia o cliente:

   ```powershell
   $env:DELIVER_HOST = "192.168.1.117"
   $env:DELIVER_PORT = "5000"
   python main.py
   ```

   Substitui `192.168.1.117` pelo IPv4 que encontraste com `ipconfig` no
   computador servidor. Escolhe `2 - Iniciar cliente`.

As variáveis `$env:...` duram apenas enquanto essa janela do PowerShell estiver
aberta. Se o IPv4 do servidor mudar, atualiza `DELIVER_HOST` no cliente.
Reserva um endereço fixo para o servidor nas definições do router se o IP mudar
frequentemente.

Não é necessário abrir a porta do MySQL no firewall: apenas o servidor acede à
base de dados localmente. Não configures encaminhamento de portas no router nem
exponhas este servidor à Internet.

## Iniciar na mesma máquina

Para executar cliente e servidor no mesmo computador, instala as dependências
e executa `python main.py` em duas janelas: escolhe `1 - Iniciar servidor` na
primeira e `2 - Iniciar cliente` na segunda. O cliente usa `127.0.0.1:5000` por
omissão.

No servidor, `DELIVER_PORT` pode alterar a porta de escuta, e
`DELIVER_BIND_HOST` pode escolher o endereço de interface. Por omissão o
servidor escuta em todas as interfaces IPv4 (`0.0.0.0`) na porta `5000`; usa
`DELIVER_BIND_HOST=127.0.0.1` apenas se quiseres restringi-lo ao próprio
computador.

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

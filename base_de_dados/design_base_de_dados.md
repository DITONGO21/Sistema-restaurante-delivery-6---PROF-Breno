# Design da Base de Dados

## 1. Introdução

A base de dados do sistema de Restaurante Delivery vai ser utilizada para guardar e gerir as informações necessárias ao funcionamento da aplicação. Foi escolhido o MySQL, como pedido no enunciado do trabalho.

A base de dados vai permitir guardar os utilizadores, os pratos disponíveis, os pedidos realizados pelos clientes e os produtos incluídos em cada pedido.

## 2. Tabelas da Base de Dados

### 2.1. Utilizadores

Esta tabela vai guardar os dados das pessoas que utilizam a aplicação, incluindo administradores, clientes e entregadores.

Os principais campos serão:
- ID do utilizador;
- Nome de utilizador;
- Palavra-passe protegida;
- Tipo de utilizador.

O tipo de utilizador será importante para distinguir as permissões de cada pessoa dentro do sistema.

### 2.2. Produtos

Esta tabela vai guardar os pratos disponíveis no restaurante.

Os campos principais serão:
- ID do produto;
- Nome do prato;
- Descrição;
- Categoria;
- Preço;
- Quantidade em stock.

O administrador será responsável por adicionar, atualizar e remover produtos. Os restantes utilizadores poderão consultar o cardápio.

### 2.3. Pedidos

Esta tabela vai guardar as informações gerais de cada encomenda realizada.

Os campos principais serão:
- ID do pedido;
- ID do cliente;
- Data do pedido;
- Estado do pedido;
- Valor total.

Cada pedido estará associado ao cliente que o realizou. O estado permitirá acompanhar a encomenda, desde a preparação até à entrega.

### 2.4. Detalhes do Pedido

Esta tabela vai guardar os produtos e as quantidades incluídas em cada pedido.

Os campos principais serão:
- ID do detalhe;
- ID do pedido;
- ID do produto;
- Quantidade;
- Preço unitário no momento da compra.

Esta tabela é necessária porque um pedido pode conter vários produtos e o mesmo produto pode aparecer em diferentes pedidos.

O preço unitário será guardado no momento da compra para que as alterações futuras aos preços não modifiquem o valor das encomendas anteriores.

## 3. Relações entre as Tabelas

A base de dados terá as seguintes relações:

- **Utilizadores e Pedidos:** um cliente pode realizar vários pedidos, mas cada pedido pertence a um único cliente.
- **Pedidos e Detalhes do Pedido:** um pedido pode ter vários detalhes, correspondendo aos diferentes produtos encomendados.
- **Produtos e Detalhes do Pedido:** um produto pode aparecer em vários detalhes de pedidos diferentes.

Estas relações serão estabelecidas através de chaves primárias e chaves estrangeiras, de forma a manter os dados organizados e evitar referências a registos inexistentes.

## 4. Regras da Base de Dados

Para evitar erros durante a utilização da aplicação, serão consideradas algumas regras:

- O preço de um produto não pode ser negativo.
- A quantidade em stock não pode ser negativa.
- A quantidade de cada produto num pedido tem de ser superior a zero.
- Cada utilizador e cada produto terão um identificador único.
- Um pedido só poderá ser confirmado se existir stock suficiente.
- Os dados de cada pedido devem ficar relacionados com o cliente que o realizou.
- As operações de venda e atualização do stock devem ser realizadas de forma consistente.

## 5. Conclusão

Esta estrutura permite organizar a informação necessária ao funcionamento do sistema de Restaurante Delivery. A separação dos dados por tabelas facilita a gestão dos produtos, dos utilizadores e das encomendas, tornando a base de dados mais organizada e permitindo futuras alterações ao projeto.
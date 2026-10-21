"""IMPORTANTE. usa este comando para criar a base de dados NO PHPMyAdmin E OS COMANDOS PARA CRIAR As TABELAS TAMBEM: 
CREATE DATABASE IF NOT EXISTS restaurante_delivery;
USE restaurante_delivery;"""

CREATE TABLE IF NOT EXISTS utilizadores (
    id_utilizador INT AUTO_INCREMENT PRIMARY KEY,
    nome_utilizador VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tipo_utilizador ENUM('cliente', 'entregador', 'admin') NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
    stock INT NOT NULL CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    data_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado ENUM(
        'pendente',
        'em preparacao',
        'em entrega',
        'entregue',
        'cancelado'
    ) NOT NULL DEFAULT 'pendente',
    valor_total DECIMAL(10,2) NOT NULL CHECK (valor_total >= 0),
    CONSTRAINT fk_pedidos_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES utilizadores(id_utilizador)
);

CREATE TABLE IF NOT EXISTS detalhes_pedido (
    id_detalhe INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
    CONSTRAINT fk_detalhes_pedido
        FOREIGN KEY (id_pedido)
        REFERENCES pedidos(id_pedido),
    CONSTRAINT fk_detalhes_produto
        FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);
CREATE TABLE clientes (
    cod_cliente INT AUTO_INCREMENT PRIMARY KEY,  
    nome VARCHAR(100) NOT NULL,                    
    email VARCHAR(100) UNIQUE NOT NULL,            
    cpf VARCHAR(11) UNIQUE NOT NULL,               
    telefone VARCHAR(15)                         
);

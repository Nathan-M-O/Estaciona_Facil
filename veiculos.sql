CREATE TABLE veiculos (
    cod_veiculo INT AUTO_INCREMENT PRIMARY KEY,   
    cod_cliente INT,                             
    placa VARCHAR(7) NOT NULL,                    
    marca VARCHAR(50),                           
    modelo VARCHAR(50),                           
    cor VARCHAR(20),                              
    FOREIGN KEY (cod_cliente) REFERENCES clientes(cod_cliente) ON DELETE CASCADE
);

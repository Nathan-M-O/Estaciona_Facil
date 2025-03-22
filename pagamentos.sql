CREATE TABLE pagamentos (
    cod_pagamento INT AUTO_INCREMENT PRIMARY KEY,                       
    cod_cliente INT,                              
    valor_pag DECIMAL(10,2) NOT NULL,             
    forma_pag VARCHAR(20) NOT NULL,               
    data_pag DATETIME DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (cod_cliente) REFERENCES clientes(cod_cliente) ON DELETE CASCADE
);

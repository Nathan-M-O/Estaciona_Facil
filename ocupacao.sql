CREATE TABLE ocupacao (
    cod_ocup INT AUTO_INCREMENT PRIMARY KEY,      
    cod_vaga INT,                                 
    cod_cliente INT,                              
    cod_veiculo INT,                              
    FOREIGN KEY (cod_vaga) REFERENCES vagas(cod_vaga) ON DELETE CASCADE,
    FOREIGN KEY (cod_cliente) REFERENCES clientes(cod_cliente) ON DELETE CASCADE,
    FOREIGN KEY (cod_veiculo) REFERENCES veiculos(cod_veiculo) ON DELETE CASCADE
);

CREATE TABLE vagas (
    cod_vaga INT AUTO_INCREMENT PRIMARY KEY,     
    numero_vaga INT NOT NULL,                      
    tipo_veiculo VARCHAR(20) NOT NULL,            
    disponibilidade BOOLEAN NOT NULL              
);

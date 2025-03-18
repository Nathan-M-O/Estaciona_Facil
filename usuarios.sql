CREATE TABLE usuarios (
    cod_usuario INT AUTO_INCREMENT PRIMARY KEY,   
    nome VARCHAR(100) NOT NULL,                    
    email VARCHAR(100) UNIQUE NOT NULL,            
    senha VARCHAR(255) NOT NULL                  
);

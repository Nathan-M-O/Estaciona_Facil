import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",  
            password="mysqlalphaone_1", 
            database="Estaciona_Facil"  
        )
        
        if conn.is_connected():
            print("Conexão com o banco de dados bem-sucedida.")
            return conn
        else:
            print("Falha na conexão com o banco de dados.")
            return None
    
    except Error as e:
        print(f"Erro ao conectar com o MySQL: {e}")
        return None
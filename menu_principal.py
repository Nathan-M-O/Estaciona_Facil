import tkinter as tk
from tkinter import messagebox
from cadastro_clientes import tela_cadastro_clientes
from gerenciamento_vagas import gerenciamento_vagas
from ocupacao import ocupacao
from pagamentos import tela_pagamento
from registro_pagamentos import exibir_historico_pagamentos
from visualizar_clientes import visualizar_clientes

def abrir_cadastro_clientes(menu_principal_window):
    tela_cadastro_clientes(menu_principal_window)

def abrir_gerenciamento_vagas():
    gerenciamento_vagas()

def abrir_visualizar_clientes():
    visualizar_clientes()

def abrir_ocupacao():
    ocupacao()

def abrir_pagamentos():
    tela_pagamento()

def abrir_historico_pagamentos():
    exibir_historico_pagamentos()

def criar_menu_principal(root):
    root.title("Menu Principal")

    root.state('zoomed')

    btn_cadastro_clientes = tk.Button(root, text="Cadastro de Clientes", command=lambda: abrir_cadastro_clientes(root), font=("Arial", 14), width=20, height=2)
    btn_cadastro_clientes.pack(pady=20)

    btn_gerenciamento_vagas = tk.Button(root, text="Gerenciamento de Vagas", command=abrir_gerenciamento_vagas, font=("Arial", 14), width=20, height=2)
    btn_gerenciamento_vagas.pack(pady=20)

    btn_visualizar_clientes = tk.Button(root, text="Visualizar Clientes", command=abrir_visualizar_clientes, font=("Arial", 14), width=20, height=2)
    btn_visualizar_clientes.pack(pady=20)

    btn_ocupacao = tk.Button(root, text="Ocupação", command=abrir_ocupacao, font=("Arial", 14), width=20, height=2)
    btn_ocupacao.pack(pady=20)

    btn_pagamentos = tk.Button(root, text="Registrar Pagamento", command=abrir_pagamentos, font=("Arial", 14), width=20, height=2)
    btn_pagamentos.pack(pady=20)

    btn_historico_pagamentos = tk.Button(root, text="Histórico de Pagamentos", command=abrir_historico_pagamentos, font=("Arial", 14), width=20, height=2)
    btn_historico_pagamentos.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk() 
    criar_menu_principal(root)
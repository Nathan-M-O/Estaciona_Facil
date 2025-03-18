import tkinter as tk
from tkinter import messagebox
from cadastro_clientes import tela_cadastro_clientes
from gerenciamento_vagas import gerenciamento_vagas
from ocupacao import exibir_ocupacoes
from pagamentos import tela_pagamento
from registro_pagamentos import exibir_historico_pagamentos
from visualizar_clientes import visualizar_clientes

def abrir_cadastro_clientes():
    tela_cadastro_clientes()

def abrir_gerenciamento_vagas():
    gerenciamento_vagas()

def abrir_visualizar_clientes():
    visualizar_clientes()

def abrir_ocupacao():
    exibir_ocupacoes()

def abrir_pagamentos():
    tela_pagamento()

def abrir_historico_pagamentos():
    exibir_historico_pagamentos()

root = tk.Tk()
root.title("Menu Principal")

root.withdraw()

btn_cadastro_clientes = tk.Button(root, text="Cadastro de Clientes", command=abrir_cadastro_clientes)
btn_cadastro_clientes.pack(pady=10)

btn_gerenciamento_vagas = tk.Button(root, text="Gerenciamento de Vagas", command=abrir_gerenciamento_vagas)
btn_gerenciamento_vagas.pack(pady=10)

btn_visualizar_clientes = tk.Button(root, text="Visualizar Clientes", command=abrir_visualizar_clientes)
btn_visualizar_clientes.pack(pady=10)

btn_ocupacao = tk.Button(root, text="Ocupação", command=abrir_ocupacao)
btn_ocupacao.pack(pady=10)

btn_pagamentos = tk.Button(root, text="Registrar Pagamento", command=abrir_pagamentos)
btn_pagamentos.pack(pady=10)

btn_historico_pagamentos = tk.Button(root, text="Histórico de Pagamentos", command=abrir_historico_pagamentos)
btn_historico_pagamentos.pack(pady=10)

root.mainloop()
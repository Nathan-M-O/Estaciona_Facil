import tkinter as tk
from tkinter import messagebox
from conexao import connect_db 

def inserir_pagamento(cod_ocupacao, cod_cliente, valor_pagamento, forma_pagamento):
    if not cod_ocupacao or not cod_cliente or not valor_pagamento or not forma_pagamento:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            query = """
                INSERT INTO pagamentos (cod_ocupacao, cod_cliente, valor_pag, forma_pag)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (cod_ocupacao, cod_cliente, valor_pagamento, forma_pagamento))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
            return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar pagamento: {e}")
        return False

def tela_pagamento():
    pagamento_window = tk.Toplevel()
    pagamento_window.title("Registrar Pagamento")

    label_cod_ocupacao = tk.Label(pagamento_window, text="Código da Ocupação:")
    label_cod_ocupacao.grid(row=0, column=0, padx=10, pady=5)
    entry_cod_ocupacao = tk.Entry(pagamento_window)
    entry_cod_ocupacao.grid(row=0, column=1, padx=10, pady=5)

    label_cod_cliente = tk.Label(pagamento_window, text="Código do Cliente:")
    label_cod_cliente.grid(row=1, column=0, padx=10, pady=5)
    entry_cod_cliente = tk.Entry(pagamento_window)
    entry_cod_cliente.grid(row=1, column=1, padx=10, pady=5)

    label_valor_pagamento = tk.Label(pagamento_window, text="Valor do Pagamento:")
    label_valor_pagamento.grid(row=2, column=0, padx=10, pady=5)
    entry_valor_pagamento = tk.Entry(pagamento_window)
    entry_valor_pagamento.grid(row=2, column=1, padx=10, pady=5)

    label_forma_pagamento = tk.Label(pagamento_window, text="Forma de Pagamento:")
    label_forma_pagamento.grid(row=3, column=0, padx=10, pady=5)
    entry_forma_pagamento = tk.Entry(pagamento_window)
    entry_forma_pagamento.grid(row=3, column=1, padx=10, pady=5)

    def registrar_pagamento():
        cod_ocupacao = entry_cod_ocupacao.get()
        cod_cliente = entry_cod_cliente.get()
        valor_pagamento = entry_valor_pagamento.get()
        forma_pagamento = entry_forma_pagamento.get()

        if inserir_pagamento(cod_ocupacao, cod_cliente, valor_pagamento, forma_pagamento):
            entry_cod_ocupacao.delete(0, 'end')
            entry_cod_cliente.delete(0, 'end')
            entry_valor_pagamento.delete(0, 'end')
            entry_forma_pagamento.delete(0, 'end')

    botao_inserir_pagamento = tk.Button(pagamento_window, text="Registrar Pagamento", command=registrar_pagamento)
    botao_inserir_pagamento.grid(row=4, column=0, columnspan=2, pady=10)

    pagamento_window.mainloop()
import tkinter as tk
from tkinter import messagebox
from conexao import connect_db

def inserir_pagamento(cod_cliente, valor_pagamento, forma_pagamento):
    if not cod_cliente or not valor_pagamento or not forma_pagamento:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            query = """
                INSERT INTO pagamentos (cod_cliente, valor_pag, forma_pag)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (cod_cliente, valor_pagamento, forma_pagamento))
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

    largura_janela = 600
    altura_janela = 600
    screen_width = pagamento_window.winfo_screenwidth()
    screen_height = pagamento_window.winfo_screenheight()

    position_top = int(screen_height / 2 - altura_janela / 2)
    position_right = int(screen_width / 2 - largura_janela / 2)
    pagamento_window.geometry(f'{largura_janela}x{altura_janela}+{position_right}+{position_top}')

    font_label = ('Arial', 14)
    font_entry = ('Arial', 14)
    font_button = ('Arial', 14, 'bold')

    label_cod_cliente = tk.Label(pagamento_window, text="Código do Cliente:", font=font_label)
    label_cod_cliente.grid(row=0, column=0, padx=10, pady=5)
    entry_cod_cliente = tk.Entry(pagamento_window, font=font_entry)
    entry_cod_cliente.grid(row=0, column=1, padx=10, pady=5)

    label_valor_pagamento = tk.Label(pagamento_window, text="Valor do Pagamento:", font=font_label)
    label_valor_pagamento.grid(row=1, column=0, padx=10, pady=5)
    entry_valor_pagamento = tk.Entry(pagamento_window, font=font_entry)
    entry_valor_pagamento.grid(row=1, column=1, padx=10, pady=5)

    label_forma_pagamento = tk.Label(pagamento_window, text="Forma de Pagamento:", font=font_label)
    label_forma_pagamento.grid(row=2, column=0, padx=10, pady=5)
    entry_forma_pagamento = tk.Entry(pagamento_window, font=font_entry)
    entry_forma_pagamento.grid(row=2, column=1, padx=10, pady=5)

    def registrar_pagamento():
        cod_cliente = entry_cod_cliente.get()
        valor_pagamento = entry_valor_pagamento.get()
        forma_pagamento = entry_forma_pagamento.get()

        if inserir_pagamento(cod_cliente, valor_pagamento, forma_pagamento):
            entry_cod_cliente.delete(0, 'end')
            entry_valor_pagamento.delete(0, 'end')
            entry_forma_pagamento.delete(0, 'end')

    botao_inserir_pagamento = tk.Button(pagamento_window, text="Registrar Pagamento", command=registrar_pagamento, font=font_button)
    botao_inserir_pagamento.grid(row=3, column=0, columnspan=2, pady=10)

    pagamento_window.mainloop()
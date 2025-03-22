import tkinter as tk
from tkinter import messagebox
from conexao import connect_db  

def excluir_pagamento(cod_pagamento, historico_window):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM pagamentos WHERE cod_pagamento = %s", (cod_pagamento,))
            conn.commit()
            conn.close()

            historico_window.destroy()

            messagebox.showinfo("Sucesso", "Pagamento excluído com sucesso!")
            exibir_historico_pagamentos()  
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir pagamento: {e}")

def exibir_historico_pagamentos():
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            query = """
                SELECT p.cod_pagamento, p.cod_cliente, p.valor_pag, p.forma_pag, p.data_pag
                FROM pagamentos p
                ORDER BY p.data_pag DESC
            """
            cursor.execute(query)
            pagamentos = cursor.fetchall()
            conn.close()

            if not pagamentos:
                messagebox.showinfo("Sem Pagamentos", "Não há pagamentos registrados.")
                return

            historico_window = tk.Toplevel()
            historico_window.title("Histórico de Pagamentos")

            headers = ["Código Pagamento", "Código Cliente", "Valor", "Forma de Pagamento", "Data do Pagamento", "Excluir"]
            for col, header in enumerate(headers):
                label = tk.Label(historico_window, text=header, font=("Arial", 10, "bold"))
                label.grid(row=0, column=col, padx=10, pady=5)

            for row, pagamento in enumerate(pagamentos, start=1):
                for col, item in enumerate(pagamento):
                    label = tk.Label(historico_window, text=item)
                    label.grid(row=row, column=col, padx=10, pady=5)

                botao_excluir = tk.Button(historico_window, text="Excluir", command=lambda cod_pagamento=pagamento[0]: excluir_pagamento(cod_pagamento, historico_window))
                botao_excluir.grid(row=row, column=len(pagamento), padx=10, pady=5)

            historico_window.mainloop()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar histórico de pagamentos: {e}")

def tela_registro_pagamentos():
    root = tk.Tk()
    root.title("Registro de Pagamentos")

    botao_historico = tk.Button(root, text="Exibir Histórico de Pagamentos", command=exibir_historico_pagamentos)
    botao_historico.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    tela_registro_pagamentos()
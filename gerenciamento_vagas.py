import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from conexao import connect_db

tree = None
window = None  

def exibir_vagas():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT cod_vaga, numero_vaga, tipo_veiculo, disponibilidade FROM vagas")
        vagas = cursor.fetchall()
        conn.close()

        for item in tree.get_children():
            tree.delete(item)

        for vaga in vagas:
            cod_vaga, numero_vaga, tipo_veiculo, disponibilidade = vaga
            disponibilidade_str = "Ocupada" if disponibilidade == 1 else "Livre"
            tree.insert("", "end", values=(numero_vaga, tipo_veiculo, disponibilidade_str))

def adicionar_vaga(entry_numero_vaga, entry_tipo_veiculo, var_disponibilidade, window):
    numero_vaga = entry_numero_vaga.get()
    tipo_veiculo = entry_tipo_veiculo.get()
    disponibilidade = var_disponibilidade.get()

    if not numero_vaga or not tipo_veiculo:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vagas (numero_vaga, tipo_veiculo, disponibilidade) VALUES (%s, %s, %s)",
            (numero_vaga, tipo_veiculo, disponibilidade)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Vaga adicionada com sucesso!")
        exibir_vagas() 
        window.destroy() 

def excluir_vaga():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma vaga para excluir!")
        return

    vaga_id = tree.item(selected_item[0], "values")[0]

    confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a vaga {vaga_id}?")
    if confirmacao:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vagas WHERE numero_vaga = %s", (vaga_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Vaga excluída com sucesso!")
            exibir_vagas()

def alterar_status_vaga():
    global window  
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma vaga para alterar o status!")
        return

    vaga_id = tree.item(selected_item[0], "values")[0]
    disponibilidade_atual = tree.item(selected_item[0], "values")[2]

    novo_status = 0 if disponibilidade_atual == "Ocupada" else 1

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE vagas SET disponibilidade = %s WHERE numero_vaga = %s", (novo_status, vaga_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Status da vaga {vaga_id} alterado!")
        exibir_vagas()  

        window.quit()  
        window.destroy()  

def gerenciamento_vagas():
    global tree, window  

    window = tk.Tk()
    window.title("Gerenciamento de Vagas")

    window.geometry("800x600")

    font_label = ('Arial', 12) 
    font_entry = ('Arial', 12)  
    font_button = ('Arial', 12, 'bold')  

    tk.Label(window, text="Número da Vaga:", font=font_label).grid(row=0, column=0)
    entry_numero_vaga = tk.Entry(window, font=font_entry, width=20)  
    entry_numero_vaga.grid(row=0, column=1)

    tk.Label(window, text="Tipo de Veículo:", font=font_label).grid(row=1, column=0)
    entry_tipo_veiculo = tk.Entry(window, font=font_entry, width=20) 
    entry_tipo_veiculo.grid(row=1, column=1)

    tk.Label(window, text="Disponibilidade:", font=font_label).grid(row=2, column=0)
    var_disponibilidade = tk.IntVar(value=0)
    tk.Radiobutton(window, text="Livre", variable=var_disponibilidade, value=0, font=font_label).grid(row=2, column=1)
    tk.Radiobutton(window, text="Ocupada", variable=var_disponibilidade, value=1, font=font_label).grid(row=2, column=2)

    tk.Button(window, text="Adicionar Vaga", font=font_button, 
          command=lambda: adicionar_vaga(entry_numero_vaga, entry_tipo_veiculo, var_disponibilidade, window)).grid(row=3, columnspan=3)

    columns = ("Número da Vaga", "Tipo de Veículo", "Disponibilidade")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.grid(row=4, columnspan=3)

    for col in columns:
        tree.heading(col, text=col)

    tk.Button(window, text="Excluir Vaga", font=font_button, command=excluir_vaga).grid(row=5, column=0)
    tk.Button(window, text="Alterar Status", font=font_button, command=alterar_status_vaga).grid(row=5, column=1)

    exibir_vagas()

    window.mainloop()
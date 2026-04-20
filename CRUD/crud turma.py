import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class SistemaTurma:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Gestão de Turmas")
        
        # Dimensões da tela
        self.largura = self.raiz.winfo_screenwidth()
        self.altura = self.raiz.winfo_screenheight()
        self.raiz.geometry(f"{self.largura}x{self.altura}+0+0")
        
        # Paleta de Cores solicitada
        self.cor_royal_blue = "#4169E1"
        self.cor_quicksand = "#BD978E"
        self.cor_shellstone = "#E5DED1"

        # Título Principal
        titulo = tk.Label(self.raiz, text="Gerenciamento de Turmas", bd=10, relief="flat", 
                         bg=self.cor_royal_blue, fg="white", font=("arial", 30, "bold"))
        titulo.pack(side="top", fill="x")

        # Painel de Opções (Lado Esquerdo - Quicksand)
        self.quadro_opcoes = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_quicksand)
        self.quadro_opcoes.place(x=20, y=100, width=self.largura//4, height=self.altura-180)

        # Botões de Operação
        botoes_texto = [
            ("Nova Turma", self.funcao_quadro_adicionar),
            ("Consultar Turma", self.funcao_quadro_busca),
            ("Editar Status/Turno", self.funcao_quadro_atualizar),
            ("Listar Todas", self.mostrar_todas),
            ("Excluir Turma", self.funcao_quadro_remover)
        ]

        for i, (texto, comando) in enumerate(botoes_texto):
            tk.Button(self.quadro_opcoes, text=texto, bd=2, relief="raised", bg=self.cor_shellstone,
                      width=20, font=("arial", 12, "bold"), command=comando).grid(row=i, column=0, padx=40, pady=20)

        # Painel de Visualização (Direita - Shellstone)
        self.quadro_visualizacao = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_shellstone)
        self.quadro_visualizacao.place(x=(self.largura//4)+50, y=100, width=(self.largura//1.5), height=self.altura-180)

        lbl_painel = tk.Label(self.quadro_visualizacao, text="Listagem de Turmas Ativas", font=("arial", 20, "bold"), 
                             bg=self.cor_shellstone, fg=self.cor_royal_blue)
        lbl_painel.pack(side="top", fill="x", pady=10)

        self.configurar_tabela()

    def conectar_db(self):
        try:
            # Certifique-se de que o banco de dados e a tabela Curso existam devido à FK
            self.conexao = pymysql.connect(host="localhost", user="root", password="SUA_SENHA", database="escola")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão com o Banco: {e}")

    def configurar_tabela(self):
        self.quadro_tab = tk.Frame(self.quadro_visualizacao, bd=2, relief="sunken")
        self.quadro_tab.place(x=10, y=60, width=(self.largura//1.6), height=self.altura-300)

        colunas = ("id", "turno", "inicio", "status", "id_curso")
        self.tabela = ttk.Treeview(self.quadro_tab, columns=colunas, show="headings")
        
        self.tabela.heading("id", text="ID Turma")
        self.tabela.heading("turno", text="Turno")
        self.tabela.heading("inicio", text="Data Início")
        self.tabela.heading("status", text="Status")
        self.tabela.heading("id_curso", text="ID Curso")

        for col in colunas:
            self.tabela.column(col, width=120, anchor="center")

        self.tabela.pack(fill="both", expand=1)

    # --- FORMULÁRIO DE CADASTRO (CREATE) ---
    def funcao_quadro_adicionar(self):
        self.janela_form = tk.Toplevel(self.raiz)
        self.janela_form.title("Cadastrar Nova Turma")
        self.janela_form.geometry("450x550")
        self.janela_form.config(bg=self.cor_quicksand)

        # Campos
        tk.Label(self.janela_form, text="Turno (manha/tarde/noite):", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.ent_turno = ttk.Combobox(self.janela_form, values=["manha", "tarde", "noite"], font=("arial", 12))
        self.ent_turno.pack(pady=5)

        tk.Label(self.janela_form, text="Data Início (AAAA-MM-DD):", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.ent_inicio = tk.Entry(self.janela_form, font=("arial", 12))
        self.ent_inicio.pack(pady=5)

        tk.Label(self.janela_form, text="Status (andamento/completo):", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.ent_status = ttk.Combobox(self.janela_form, values=["andamento", "completo"], font=("arial", 12))
        self.ent_status.pack(pady=5)

        tk.Label(self.janela_form, text="ID do Curso (FK):", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.ent_curso = tk.Entry(self.janela_form, font=("arial", 12))
        self.ent_curso.pack(pady=5)

        tk.Button(self.janela_form, text="Salvar Turma", bg=self.cor_royal_blue, fg="white", 
                  font=("arial", 12, "bold"), command=self.salvar_turma).pack(pady=30)

    def salvar_turma(self):
        try:
            self.conectar_db()
            query = "INSERT INTO Turma (Turno, Data_inicio, turma_status, ID_Curso) VALUES (%s, %s, %s, %s)"
            valores = (self.ent_turno.get(), self.ent_inicio.get(), self.ent_status.get(), self.ent_curso.get())
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Turma registrada com sucesso!")
            self.janela_form.destroy()
            self.mostrar_todas()
        except Exception as e:
            messagebox.showerror("Erro SQL", f"Erro ao inserir: {e}")

    # --- LEITURA (READ) ---
    def mostrar_todas(self):
        try:
            self.conectar_db()
            self.cursor.execute("SELECT * FROM Turma")
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar: {e}")

    # --- ATUALIZAÇÃO (UPDATE) ---
    def funcao_quadro_atualizar(self):
        self.janela_atua = tk.Toplevel(self.raiz)
        self.janela_atua.title("Atualizar Turma")
        self.janela_atua.geometry("400x300")
        self.janela_atua.config(bg=self.cor_quicksand)

        tk.Label(self.janela_atua, text="ID da Turma para mudar:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.id_mudar = tk.Entry(self.janela_atua, font=("arial", 12))
        self.id_mudar.pack(pady=5)

        tk.Label(self.janela_atua, text="Novo Status:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
        self.novo_status = ttk.Combobox(self.janela_atua, values=["andamento", "completo"], font=("arial", 12))
        self.novo_status.pack(pady=5)

        tk.Button(self.janela_atua, text="Atualizar Status", bg=self.cor_royal_blue, fg="white", 
                  command=self.executar_update).pack(pady=20)

    def executar_update(self):
        try:
            self.conectar_db()
            query = "UPDATE Turma SET turma_status = %s WHERE ID_Turma = %s"
            self.cursor.execute(query, (self.novo_status.get(), self.id_mudar.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Status atualizado!")
            self.janela_atua.destroy()
            self.mostrar_todas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- REMOÇÃO (DELETE) ---
    def funcao_quadro_remover(self):
        self.janela_del = tk.Toplevel(self.raiz)
        self.janela_del.geometry("300x200")
        self.janela_del.config(bg=self.cor_quicksand)
        
        tk.Label(self.janela_del, text="ID Turma para Excluir:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=20)
        self.id_del = tk.Entry(self.janela_del, font=("arial", 12))
        self.id_del.pack()
        
        tk.Button(self.janela_del, text="Confirmar Exclusão", bg="red", fg="white", 
                  command=self.executar_delete).pack(pady=20)

    def executar_delete(self):
        try:
            self.conectar_db()
            self.cursor.execute("DELETE FROM Turma WHERE ID_Turma = %s", (self.id_del.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Aviso", "Turma excluída!")
            self.janela_del.destroy()
            self.mostrar_todas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def funcao_quadro_busca(self):
        # Lógica de busca similar à anterior, filtrando por ID ou Turno
        pass

if __name__ == "__main__":
    raiz = tk.Tk()
    app = SistemaTurma(raiz)
    raiz.mainloop()

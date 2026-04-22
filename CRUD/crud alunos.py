import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
import hashlib

class SistemaEstudante:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Cadastro de Estudantes - CRUD Completo")
        
        self.largura = self.raiz.winfo_screenwidth()
        self.altura = self.raiz.winfo_screenheight()
        self.raiz.geometry(f"{self.largura}x{self.altura}+0+0")
        
        self.cor_royal_blue = "#112250"
        self.cor_quicksand = "#E0BE7A"
        self.cor_shellstone = "#D9CBC2"

        titulo = tk.Label(self.raiz, text="Gerenciamento de Dados do Aluno", bd=10, relief="flat",
                         bg=self.cor_royal_blue, fg="white", font=("arial", 30, "bold"))
        titulo.pack(side="top", fill="x")

        self.quadro_opcoes = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_quicksand)
        self.quadro_opcoes.place(x=20, y=100, width=self.largura//4, height=self.altura-180)
        self.quadro_opcoes.grid_columnconfigure(0, weight=1)

        botoes_texto = [
            ("Novo Cadastro", self.funcao_quadro_adicionar),
            ("Consultar Aluno", self.funcao_quadro_busca),
            ("Editar Registro", self.funcao_quadro_atualizar),
            ("Listar Todos", self.mostrar_todos),
            ("Remover Registro", self.funcao_quadro_remover)
        ]

        for i, (texto, comando) in enumerate(botoes_texto):
            tk.Button(self.quadro_opcoes, text=texto, bd=2, relief="raised", bg=self.cor_shellstone,
                      width=18, font=("arial", 12, "bold"), command=comando).grid(row=i, column=0, padx=10, pady=20, sticky="n")

        self.quadro_visualizacao = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_shellstone)
        self.quadro_visualizacao.place(x=(self.largura//4)+50, y=100, width=(self.largura//1.5), height=self.altura-180)

        lbl_painel = tk.Label(self.quadro_visualizacao, text="Base de Dados de Alunos", font=("arial", 20, "bold"),
                             bg=self.cor_shellstone, fg=self.cor_royal_blue)
        lbl_painel.pack(side="top", fill="x", pady=10)

        self.configurar_tabela()

    def conectar_db(self):
        try:
            self.conexao = pymysql.connect(host="localhost", user="root", password="", database="sistema_facil")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {e}")

    def configurar_tabela(self):
        self.quadro_tab = tk.Frame(self.quadro_visualizacao, bd=2, relief="sunken")
        self.quadro_tab.place(x=10, y=60, width=(self.largura//1.6), height=self.altura-300)

        colunas = ("id", "nome", "email", "endereco", "cpf", "telefone")
        self.tabela = ttk.Treeview(self.quadro_tab, columns=colunas, show="headings")
        
        cabecalhos = {"id": "ID", "nome": "Nome", "email": "Email", "endereco": "Endereço", "cpf": "CPF (Hash)", "telefone": "Telefone"}
        for col, texto in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=100, anchor="center")
        self.tabela.pack(fill="both", expand=1)

    def mascarar_cpf(self, cpf):
        return hashlib.sha256(cpf.encode()).hexdigest()

    # --- CREATE (ADICIONAR) - MANTIDO CONFORME SOLICITADO ---
    def funcao_quadro_adicionar(self):
        self.janela_form = tk.Toplevel(self.raiz)
        self.janela_form.title("Novo Cadastro")
        self.janela_form.geometry("450x500")
        self.janela_form.config(bg=self.cor_quicksand)

        labels = ["Nome", "Email", "Endereço", "CPF", "Telefone"]
        self.entradas = {}

        for i, texto in enumerate(labels):
            tk.Label(self.janela_form, text=f"{texto}:", bg=self.cor_quicksand, font=("arial", 12, "bold")).grid(row=i, column=0, padx=20, pady=15)
            ent = tk.Entry(self.janela_form, font=("arial", 12), bd=2)
            ent.grid(row=i, column=1, padx=10, pady=15)
            chave = texto.lower().replace(" ", "_").replace("é", "e").replace("ç", "c").replace("õ", "o")
            self.entradas[chave] = ent

        btn_salvar = tk.Button(self.janela_form, text="Salvar Cadastro", bg=self.cor_royal_blue, fg="white",
                              font=("arial", 12, "bold"), command=self.salvar_dados)
        btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def salvar_dados(self):
        try:
            self.conectar_db()
            query = "INSERT INTO aluno (nome, email, endereco, CPF, telefone) VALUES (%s, %s, %s, %s, %s)"
            valores = (
                self.entradas['nome'].get(), self.entradas['email'].get(),
                self.entradas['endereco'].get(), self.mascarar_cpf(self.entradas['cpf'].get()),
                self.entradas['telefone'].get()
            )
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Estudante cadastrado!")
            self.janela_form.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    # --- READ (BUSCAR) ---
    def funcao_quadro_busca(self):
        self.janela_busca = tk.Toplevel(self.raiz)
        self.janela_busca.title("Buscar Aluno")
        self.janela_busca.geometry("400x300")
        self.janela_busca.config(bg=self.cor_quicksand)

        tk.Label(self.janela_busca, text="Buscar por Nome:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=10)
        self.ent_busca_nome = tk.Entry(self.janela_busca, font=("arial", 12))
        self.ent_busca_nome.pack(pady=5)

        tk.Button(self.janela_busca, text="Pesquisar", bg=self.cor_royal_blue, fg="white", command=self.executar_busca).pack(pady=20)

    def executar_busca(self):
        try:
            self.conectar_db()
            query = "SELECT * FROM aluno WHERE nome LIKE %s"
            self.cursor.execute(query, (f"%{self.ent_busca_nome.get()}%"))
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
            self.janela_busca.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Busca falhou: {e}")

    # --- UPDATE (ATUALIZAR) ---
    def funcao_quadro_atualizar(self):
        self.janela_atua = tk.Toplevel(self.raiz)
        self.janela_atua.title("Editar Aluno")
        self.janela_atua.geometry("450x450")
        self.janela_atua.config(bg=self.cor_quicksand)

        tk.Label(self.janela_atua, text="ID do Aluno para editar:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=5)
        self.id_editar = tk.Entry(self.janela_atua)
        self.id_editar.pack()

        tk.Label(self.janela_atua, text="Novo E-mail:", bg=self.cor_quicksand).pack(pady=5)
        self.novo_email = tk.Entry(self.janela_atua)
        self.novo_email.pack()

        tk.Label(self.janela_atua, text="Novo Endereço:", bg=self.cor_quicksand).pack(pady=5)
        self.novo_endereco = tk.Entry(self.janela_atua)
        self.novo_endereco.pack()

        tk.Button(self.janela_atua, text="Atualizar Dados", bg=self.cor_royal_blue, fg="white", command=self.executar_atualizacao).pack(pady=20)

    def executar_atualizacao(self):
        try:
            self.conectar_db()
            query = "UPDATE aluno SET email=%s, endereco=%s WHERE id_aluno=%s"
            self.cursor.execute(query, (self.novo_email.get(), self.novo_endereco.get(), self.id_editar.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Registro atualizado!")
            self.janela_atua.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

    # --- DELETE (REMOVER) ---
    def funcao_quadro_remover(self):
        self.janela_rem = tk.Toplevel(self.raiz)
        self.janela_rem.title("Remover Aluno")
        self.janela_rem.geometry("300x200")
        self.janela_rem.config(bg=self.cor_quicksand)

        tk.Label(self.janela_rem, text="ID para Excluir:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=20)
        self.ent_id_rem = tk.Entry(self.janela_rem, font=("arial", 12))
        self.ent_id_rem.pack()

        tk.Button(self.janela_rem, text="Confirmar Exclusão", bg="red", fg="white", command=self.executar_remocao).pack(pady=20)

    def executar_remocao(self):
        try:
            self.conectar_db()
            query = "DELETE FROM aluno WHERE id_aluno=%s"
            self.cursor.execute(query, (self.ent_id_rem.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Aviso", "Aluno removido com sucesso!")
            self.janela_rem.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def mostrar_todos(self):
        try:
            self.conectar_db()
            self.cursor.execute("SELECT * FROM aluno")
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
        except Exception as e:
            print(f"Erro ao listar: {e}")

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaEstudante(janela)
    janela.mainloop()

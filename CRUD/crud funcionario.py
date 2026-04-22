import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class SistemaFuncionario:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Gestão de Funcionários")
        
        # Dimensões da tela
        self.largura = self.raiz.winfo_screenwidth()
        self.altura = self.raiz.winfo_screenheight()
        self.raiz.geometry(f"{self.largura}x{self.altura}+0+0")
        
        # Paleta de Cores
        self.cor_royal_blue = "#112250"
        self.cor_quicksand = "#C78950"
        self.cor_shellstone = "#E5DED1"

        # Título Principal
        titulo = tk.Label(self.raiz, text="Gerenciamento de Funcionários", bd=10, relief="flat", 
                         bg=self.cor_royal_blue, fg="white", font=("arial", 30, "bold"))
        titulo.pack(side="top", fill="x")

        # Painel de Opções (Lado Esquerdo - Quicksand)
        self.quadro_opcoes = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_quicksand)
        self.quadro_opcoes.place(x=20, y=100, width=self.largura//4, height=self.altura-180)

        # Botões de Operação
        botoes_texto = [
            ("Novo Funcionário", self.funcao_quadro_adicionar),
            ("Consultar Cadastro", self.mostrar_todos),
            ("Atualizar Dados", self.funcao_quadro_atualizar),
            ("Remover Acesso", self.funcao_quadro_remover)
        ]

        for i, (texto, comando) in enumerate(botoes_texto):
            tk.Button(self.quadro_opcoes, text=texto, bd=2, relief="raised", bg=self.cor_shellstone,
                      width=20, font=("arial", 12, "bold"), command=comando).grid(row=i, column=0, padx=40, pady=25)

        # Painel de Visualização (Direita - Shellstone)
        self.quadro_visualizacao = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_shellstone)
        self.quadro_visualizacao.place(x=(self.largura//4)+50, y=100, width=(self.largura//1.5), height=self.altura-180)

        lbl_painel = tk.Label(self.quadro_visualizacao, text="Quadro de Funcionários Ativos", font=("arial", 20, "bold"), 
                             bg=self.cor_shellstone, fg=self.cor_royal_blue)
        lbl_painel.pack(side="top", fill="x", pady=10)

        self.configurar_tabela()

    def conectar_db(self):
        try:
            # Substitua 'SUA_SENHA' pela sua senha real do MySQL
            self.conexao = pymysql.connect(host="localhost", user="root", password="SUA_SENHA", database="empresa")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Falha: {e}")

    def configurar_tabela(self):
        self.quadro_tab = tk.Frame(self.quadro_visualizacao, bd=2, relief="sunken")
        self.quadro_tab.place(x=10, y=60, width=(self.largura//1.6), height=self.altura-300)

        colunas = ("id", "nome", "email", "endereco", "cpf", "telefone", "id_venda")
        self.tabela = ttk.Treeview(self.quadro_tab, columns=colunas, show="headings")
        
        cabecalhos = ["ID", "Nome", "E-mail", "Endereço", "CPF", "Telefone", "Ref. Venda"]
        for col, cab in zip(colunas, cabecalhos):
            self.tabela.heading(col, text=cab)
            self.tabela.column(col, width=100, anchor="center")

        self.tabela.pack(fill="both", expand=1)

    # --- CADASTRO (CREATE) ---
    def funcao_quadro_adicionar(self):
        self.janela_form = tk.Toplevel(self.raiz)
        self.janela_form.title("Ficha de Funcionário")
        self.janela_form.geometry("500x700")
        self.janela_form.config(bg=self.cor_quicksand)

        campos = ["Nome", "Email", "Endereco", "CPF", "Telefone", "Senha", "ID_Venda"]
        self.entradas = {}

        for i, texto in enumerate(campos):
            tk.Label(self.janela_form, text=f"{texto}:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=2)
            # Se for o campo senha, usamos o caractere de máscara
            if texto == "Senha":
                ent = tk.Entry(self.janela_form, font=("arial", 11), show="*")
            else:
                ent = tk.Entry(self.janela_form, font=("arial", 11))
            ent.pack(pady=5)
            self.entradas[texto.lower()] = ent

        tk.Button(self.janela_form, text="Confirmar Registro", bg=self.cor_royal_blue, fg="white", 
                  font=("arial", 12, "bold"), command=self.salvar_funcionario).pack(pady=20)

    def salvar_funcionario(self):
        try:
            self.conectar_db()
            query = "INSERT INTO Funcionario (Nome, Email, Endereco, CPF, Telefone, Senha, ID_Venda) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                self.entradas['nome'].get(), self.entradas['email'].get(),
                self.entradas['endereco'].get(), self.entradas['cpf'].get(),
                self.entradas['telefone'].get(), self.entradas['senha'].get(),
                self.entradas['id_venda'].get()
            )
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.janela_form.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro SQL", str(e))

    # --- LEITURA (READ) ---
    def mostrar_todos(self):
        try:
            self.conectar_db()
            self.cursor.execute("SELECT ID_Funcionario, Nome, Email, Endereco, CPF, Telefone, ID_Venda FROM Funcionario")
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- ATUALIZAÇÃO (UPDATE) ---
    def funcao_quadro_atualizar(self):
        # Janela simples para atualizar o telefone do funcionário via ID
        self.janela_atua = tk.Toplevel(self.raiz)
        self.janela_atua.geometry("350x250")
        self.janela_atua.config(bg=self.cor_quicksand)

        tk.Label(self.janela_atua, text="ID do Funcionário:", bg=self.cor_quicksand).pack(pady=10)
        self.id_atua = tk.Entry(self.janela_atua)
        self.id_atua.pack()

        tk.Label(self.janela_atua, text="Novo Telefone:", bg=self.cor_quicksand).pack(pady=10)
        self.novo_tel = tk.Entry(self.janela_atua)
        self.novo_tel.pack()

        tk.Button(self.janela_atua, text="Atualizar", command=self.executar_update).pack(pady=20)

    def executar_update(self):
        try:
            self.conectar_db()
            query = "UPDATE Funcionario SET Telefone = %s WHERE ID_Funcionario = %s"
            self.cursor.execute(query, (self.novo_tel.get(), self.id_atua.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Dados atualizados!")
            self.janela_atua.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # --- REMOÇÃO (DELETE) ---
    def funcao_quadro_remover(self):
        self.janela_del = tk.Toplevel(self.raiz)
        self.janela_del.geometry("300x150")
        self.janela_del.config(bg=self.cor_quicksand)
        
        tk.Label(self.janela_del, text="ID para Deletar:", bg=self.cor_quicksand).pack(pady=10)
        self.id_del = tk.Entry(self.janela_del)
        self.id_del.pack()
        
        tk.Button(self.janela_del, text="Excluir", bg="red", fg="white", command=self.executar_delete).pack(pady=10)

    def executar_delete(self):
        try:
            self.conectar_db()
            self.cursor.execute("DELETE FROM Funcionario WHERE ID_Funcionario = %s", (self.id_del.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Aviso", "Funcionário removido do sistema.")
            self.janela_del.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    raiz = tk.Tk()
    app = SistemaFuncionario(raiz)
    raiz.mainloop()

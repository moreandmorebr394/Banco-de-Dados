import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class SistemaEstudante:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Cadastro de Estudantes")
        
        # Dimensões da tela
        self.largura = self.raiz.winfo_screenwidth()
        self.altura = self.raiz.winfo_screenheight()
        self.raiz.geometry(f"{self.largura}x{self.altura}+0+0")
        
        # Cores solicitadas
        self.cor_royal_blue = "#4169E1"
        self.cor_quicksand = "#BD978E"
        self.cor_shellstone = "#E5DED1"

        # Título Principal
        titulo = tk.Label(self.raiz, text="Gerenciamento de Dados do Aluno", bd=10, relief="flat", 
                         bg=self.cor_royal_blue, fg="white", font=("arial", 30, "bold"))
        titulo.pack(side="top", fill="x")

        # Painel de Opções (Esquerda)
        self.quadro_opcoes = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_quicksand)
        self.quadro_opcoes.place(x=20, y=100, width=self.largura//4, height=self.altura-180)

        # Botões de Navegação
        botoes_texto = [
            ("Novo Cadastro", self.funcao_quadro_adicionar),
            ("Consultar Aluno", self.funcao_quadro_busca),
            ("Editar Registro", self.funcao_quadro_atualizar),
            ("Listar Todos", self.mostrar_todos),
            ("Remover Registro", self.funcao_quadro_remover)
        ]

        for i, (texto, comando) in enumerate(botoes_texto):
            tk.Button(self.quadro_opcoes, text=texto, bd=2, relief="raised", bg=self.cor_shellstone,
                      width=18, font=("arial", 12, "bold"), command=comando).grid(row=i, column=0, padx=40, pady=20)

        # Painel de Visualização (Direita)
        self.quadro_visualizacao = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_shellstone)
        self.quadro_visualizacao.place(x=(self.largura//4)+50, y=100, width=(self.largura//1.5), height=self.altura-180)

        lbl_painel = tk.Label(self.quadro_visualizacao, text="Base de Dados de Alunos", font=("arial", 20, "bold"), 
                             bg=self.cor_shellstone, fg=self.cor_royal_blue)
        lbl_painel.pack(side="top", fill="x", pady=10)

        self.configurar_tabela()

    def conectar_db(self):
        try:
            self.conexao = pymysql.connect(host="localhost", user="root", password="SUA_SENHA", database="escola")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {e}")

    def configurar_tabela(self):
        self.quadro_tab = tk.Frame(self.quadro_visualizacao, bd=2, relief="sunken")
        self.quadro_tab.place(x=10, y=60, width=(self.largura//1.6), height=self.altura-300)

        colunas = ("matricula", "nome", "nome_mae", "email", "telefone", "endereco", "cpf")
        self.tabela = ttk.Treeview(self.quadro_tab, columns=colunas, show="headings")
        
        # Definição dos cabeçalhos
        cabecalhos = {
            "matricula": "Matrícula", "nome": "Nome", "nome_mae": "Nome da Mãe",
            "email": "E-mail", "telefone": "Telefone", "endereco": "Endereço", "cpf": "CPF"
        }
        for col, texto in cabecalhos.items():
            self.tabela.heading(col, text=texto)
            self.tabela.column(col, width=100)

        self.tabela.pack(fill="both", expand=1)

    # --- FORMULÁRIO DE CADASTRO ---
    def funcao_quadro_adicionar(self):
        self.janela_form = tk.Toplevel(self.raiz)
        self.janela_form.title("Formulário de Entrada")
        self.janela_form.geometry("500x600")
        self.janela_form.config(bg=self.cor_quicksand)

        labels = ["Matrícula", "Nome", "Nome da Mãe", "E-mail", "Telefone", "Endereço", "CPF"]
        self.entradas = {}

        for i, texto in enumerate(labels):
            tk.Label(self.janela_form, text=f"{texto}:", bg=self.cor_quicksand, font=("arial", 12, "bold")).grid(row=i, column=0, padx=20, pady=15)
            ent = tk.Entry(self.janela_form, font=("arial", 12), bd=2)
            ent.grid(row=i, column=1, padx=10, pady=15)
            self.entradas[texto.lower().replace(" ", "_").replace("ê", "e").replace("í", "i").replace("-", "")] = ent

        btn_salvar = tk.Button(self.janela_form, text="Salvar Cadastro", bg=self.cor_royal_blue, fg="white", 
                              font=("arial", 12, "bold"), command=self.salvar_dados)
        btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def salvar_dados(self):
        try:
            self.conectar_db()
            query = "INSERT INTO alunos VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                self.entradas['matricula'].get(), self.entradas['nome'].get(),
                self.entradas['nome_da_mae'].get(), self.entradas['email'].get(),
                self.entradas['telefone'].get(), self.entradas['endereco'].get(),
                self.entradas['cpf'].get()
            )
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Estudante cadastrado!")
            self.janela_form.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def mostrar_todos(self):
        self.conectar_db()
        self.cursor.execute("SELECT * FROM alunos")
        linhas = self.cursor.fetchall()
        self.tabela.delete(*self.tabela.get_children())
        for linha in linhas:
            self.tabela.insert('', tk.END, values=linha)
        self.conexao.close()

    # (As funções de busca, atualizar e remover seguem a mesma lógica de substituição de campos)
    def funcao_quadro_busca(self): pass
    def funcao_quadro_atualizar(self): pass
    def funcao_quadro_remover(self): pass

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaEstudante(janela)
    janela.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class SistemaCurso:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Sistema de Gestão de Cursos - CRUD Final")
        
        # Dimensões da tela
        self.largura = self.raiz.winfo_screenwidth()
        self.altura = self.raiz.winfo_screenheight()
        self.raiz.geometry(f"{self.largura}x{self.altura}+0+0")
        
        # Paleta de Cores
        self.cor_royal_blue = "#112250"
        self.cor_quicksand = "#E0BE7A"
        self.cor_shellstone = "#D9CBC2"

        # Título Principal
        titulo = tk.Label(self.raiz, text="Gerenciamento de Cursos", bd=10, relief="flat",
                         bg=self.cor_royal_blue, fg="white", font=("arial", 30, "bold"))
        titulo.pack(side="top", fill="x")

        # Painel de Opções (Lado Esquerdo)
        self.quadro_opcoes = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_quicksand)
        self.quadro_opcoes.place(x=20, y=100, width=self.largura//4, height=self.altura-180)
        
        # Centralização dos botões
        self.quadro_opcoes.grid_columnconfigure(0, weight=1)

        # Botões de Operação
        botoes_texto = [
            ("Novo Curso", self.funcao_quadro_adicionar),
            ("Consultar Curso", self.funcao_quadro_busca),
            ("Editar Registro", self.funcao_quadro_atualizar),
            ("Listar Todos", self.mostrar_todos),
            ("Excluir Curso", self.funcao_quadro_remover)
        ]

        for i, (texto, comando) in enumerate(botoes_texto):
            tk.Button(self.quadro_opcoes, text=texto, bd=2, relief="raised", bg=self.cor_shellstone,
                      width=20, font=("arial", 12, "bold"), command=comando).grid(row=i, column=0, padx=10, pady=20)

        # Painel de Visualização (Direita)
        self.quadro_visualizacao = tk.Frame(self.raiz, bd=5, relief="flat", bg=self.cor_shellstone)
        self.quadro_visualizacao.place(x=(self.largura//4)+50, y=100, width=(self.largura//1.5), height=self.altura-180)

        lbl_painel = tk.Label(self.quadro_visualizacao, text="Base de Dados de Cursos", font=("arial", 20, "bold"),
                             bg=self.cor_shellstone, fg=self.cor_royal_blue)
        lbl_painel.pack(side="top", fill="x", pady=10)

        self.configurar_tabela()

    def conectar_db(self):
        try:
            self.conexao = pymysql.connect(host="localhost", user="root", password="", database="sistema_facil")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Falha: {e}")

    def configurar_tabela(self):
        self.quadro_tab = tk.Frame(self.quadro_visualizacao, bd=2, relief="sunken")
        self.quadro_tab.place(x=10, y=60, width=(self.largura//1.6), height=self.altura-300)

        colunas = ("id", "nome", "duracao", "carga", "tipo")
        self.tabela = ttk.Treeview(self.quadro_tab, columns=colunas, show="headings")
        
        cabecalhos = ["ID", "Nome", "Duração", "Carga Horaria", "Tipo"]
        for col, cab in zip(colunas, cabecalhos):
            self.tabela.heading(col, text=cab)
            self.tabela.column(col, width=120, anchor="center")

        self.tabela.pack(fill="both", expand=1)

    # --- CREATE (ADICIONAR) ---
    def funcao_quadro_adicionar(self):
        self.janela_form = tk.Toplevel(self.raiz)
        self.janela_form.title("Cadastrar Novo Curso")
        self.janela_form.geometry("450x500")
        self.janela_form.config(bg=self.cor_quicksand)

        labels = ["Nome", "Duração", "Carga Horario", "Tipo Curso"]
        self.entradas = {}

        for i, texto in enumerate(labels):
            tk.Label(self.janela_form, text=f"{texto}:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=5)
            if texto == "Tipo Curso":
                ent = ttk.Combobox(self.janela_form, values=["capacitacao", "livre", "tecnico"], font=("arial", 12), state="readonly")
            else:
                ent = tk.Entry(self.janela_form, font=("arial", 12), bd=2)
            ent.pack(pady=5)
            chave = texto.lower().replace(" ", "_").replace("ç", "c").replace("ã", "a").replace("ó", "o")
            self.entradas[chave] = ent

        tk.Button(self.janela_form, text="Salvar Curso", bg=self.cor_royal_blue, fg="white",
                  font=("arial", 12, "bold"), command=self.salvar_dados).pack(pady=30)

    def salvar_dados(self):
        try:
            self.conectar_db()
            query = "INSERT INTO curso (nome, duracao, carga_horario, tipo_curso) VALUES (%s, %s, %s, %s)"
            valores = (self.entradas['nome'].get(), self.entradas['duracao'].get(), self.entradas['carga_horario'].get(), self.entradas['tipo_curso'].get())
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Sucesso", "Curso cadastrado!")
            self.janela_form.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro SQL", f"Falha: {e}")

    # --- READ (BUSCAR) ---
    def funcao_quadro_busca(self):
        self.janela_busca = tk.Toplevel(self.raiz)
        self.janela_busca.title("Consultar Curso")
        self.janela_busca.geometry("400x300")
        self.janela_busca.config(bg=self.cor_quicksand)

        tk.Label(self.janela_busca, text="Digite o nome do curso:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=20)
        self.ent_busca = tk.Entry(self.janela_busca, font=("arial", 12), bd=2)
        self.ent_busca.pack(pady=10)

        tk.Button(self.janela_busca, text="Buscar no Banco", bg=self.cor_royal_blue, fg="white", 
                  font=("arial", 11, "bold"), command=self.executar_busca).pack(pady=20)

    def executar_busca(self):
        try:
            self.conectar_db()
            # Busca flexível por nome
            query = "SELECT * FROM curso WHERE nome LIKE %s"
            self.cursor.execute(query, (f"%{self.ent_busca.get()}%"))
            linhas = self.cursor.fetchall()
            
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            
            self.conexao.close()
            self.janela_busca.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {e}")

    # --- READ (LISTAR TUDO) ---
    def mostrar_todos(self):
        try:
            self.conectar_db()
            self.cursor.execute("SELECT * FROM curso")
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar: {e}")

    # --- UPDATE (EDITAR) ---
    def funcao_quadro_atualizar(self):
        self.janela_atua = tk.Toplevel(self.raiz)
        self.janela_atua.title("Editar Curso")
        self.janela_atua.geometry("450x600")
        self.janela_atua.config(bg=self.cor_quicksand)

        tk.Label(self.janela_atua, text="ID do Curso para editar:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=5)
        self.id_editar = tk.Entry(self.janela_atua, font=("arial", 12), bd=2)
        self.id_editar.pack(pady=5)

        tk.Label(self.janela_atua, text="Novo Nome:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=5)
        self.novo_nome = tk.Entry(self.janela_atua, font=("arial", 12), bd=2)
        self.novo_nome.pack(pady=5)

        tk.Label(self.janela_atua, text="Nova Duração:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=5)
        self.nova_duracao = tk.Entry(self.janela_atua, font=("arial", 12), bd=2)
        self.nova_duracao.pack(pady=5)

        tk.Label(self.janela_atua, text="Nova Carga Horaria:", bg=self.cor_quicksand, font=("arial", 11, "bold")).pack(pady=5)
        self.nova_carga = tk.Entry(self.janela_atua, font=("arial", 12), bd=2)
        self.nova_carga.pack(pady=5)

        tk.Button(self.janela_atua, text="Confirmar Edição", bg=self.cor_royal_blue, fg="white", 
                  font=("arial", 12, "bold"), command=self.executar_atualizacao).pack(pady=30)

    def executar_atualizacao(self):
        try:
            self.conectar_db()
            query = "UPDATE curso SET nome=%s, duracao=%s, carga_horario=%s WHERE id_curso=%s"
            valores = (self.novo_nome.get(), self.nova_duracao.get(), self.nova_carga.get(), self.id_editar.get())
            self.cursor.execute(query, valores)
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
        self.janela_rem.title("Excluir Curso")
        self.janela_rem.geometry("300x200")
        self.janela_rem.config(bg=self.cor_quicksand)

        tk.Label(self.janela_rem, text="ID para Excluir:", bg=self.cor_quicksand, font=("arial", 12, "bold")).pack(pady=20)
        self.ent_id_rem = tk.Entry(self.janela_rem, font=("arial", 12), bd=2)
        self.ent_id_rem.pack()

        tk.Button(self.janela_rem, text="Remover", bg="red", fg="white", command=self.executar_remocao).pack(pady=20)

    def executar_remocao(self):
        try:
            self.conectar_db()
            query = "DELETE FROM curso WHERE id_curso=%s"
            self.cursor.execute(query, (self.ent_id_rem.get()))
            self.conexao.commit()
            self.conexao.close()
            messagebox.showinfo("Aviso", "Curso removido!")
            self.janela_rem.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCurso(janela)
    janela.mainloop()

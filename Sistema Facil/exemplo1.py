import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class Estudante:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Estudantes")
        
        # Variáveis globais para as dimensões da tela
        self.largura = self.root.winfo_screenwidth()
        self.altura = self.root.winfo_screenheight()
        self.root.geometry(f"{self.largura}x{self.altura}+0+0")

        # Título principal da interface
        titulo = tk.Label(self.root, text="Sistema de Gerenciamento de Registros de Estudantes", bd=4, relief="raised", 
                         bg="lightgreen", font=("elephant", 30, "bold"))
        titulo.pack(side="top", fill="x")

        # Função auxiliar para gerar cores hexadecimais (RGB para Hex)
        def cor(self, r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'

        # Painel de Opções (Lado Esquerdo)
        self.quadro_opcoes = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(230, 150, 200))
        self.quadro_opcoes.place(x=50, y=100, width=self.largura//3, height=self.altura-180)

        # Botões do Painel de Opções
        btn_adicionar = tk.Button(self.quadro_opcoes, text="Adicionar Estudante", bd=3, relief="raised", bg="lightgrey",
                            width=20, font=("arial", 15, "bold"), command=self.funcao_quadro_adicionar)
        btn_adicionar.grid(row=0, column=0, padx=30, pady=25)

        btn_buscar = tk.Button(self.quadro_opcoes, text="Buscar Estudante", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.funcao_quadro_busca)
        btn_buscar.grid(row=1, column=0, padx=30, pady=25)

        btn_atualizar = tk.Button(self.quadro_opcoes, text="Atualizar Registro", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.funcao_quadro_atualizar)
        btn_atualizar.grid(row=2, column=0, padx=30, pady=25)

        btn_mostrar_todos = tk.Button(self.quadro_opcoes, text="Mostrar Todos", bd=3, relief="raised", bg="lightgrey",
                                 width=20, font=("arial", 15, "bold"), command=self.mostrar_todos)
        btn_mostrar_todos.grid(row=3, column=0, padx=30, pady=25)

        btn_remover = tk.Button(self.quadro_opcoes, text="Remover Estudante", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.funcao_quadro_remover)
        btn_remover.grid(row=4, column=0, padx=30, pady=25)

        # Painel de Detalhes e Visualização (Lado Direito)
        self.quadro_detalhes = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(150, 230, 120))
        self.quadro_detalhes.place(x=(self.largura//3)+100, y=100, width=(self.largura//2)+50, height=self.altura-180)

        lbl_detalhe = tk.Label(self.quadro_detalhes, text="Detalhes do Registro", font=("arial", 30, "bold"), 
                              bg=self.cor_rgb(150, 230, 120))
        lbl_detalhe.pack(side="top", fill="x")

        # Inicialização da tabela de dados
        self.funcao_tabela()

    def cor_rgb(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def funcao_banco_dados(self):
        """Estabelece conexão com o servidor MySQL local"""
        try:
            self.conexao = pymysql.connect(host="localhost", user="root", password="SUA_SENHA_AQUI", database="registro")
            self.cursor = self.conexao.cursor()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados: {e}")

    def funcao_tabela(self):
        """Configura a visualização da tabela (Treeview) e barras de rolagem"""
        self.quadro_tab = tk.Frame(self.quadro_detalhes, bd=4, relief="sunken", bg="cyan")
        self.quadro_tab.place(x=23, y=70, width=(self.largura//2), height=self.altura-280)

        barra_rolagem_x = tk.Scrollbar(self.quadro_tab, orient="horizontal")
        barra_rolagem_v = tk.Scrollbar(self.quadro_tab, orient="vertical")

        self.tabela = ttk.Treeview(self.quadro_tab, columns=("matricula", "nome", "nome_pai", "disciplina", "nota"),
                                  xscrollcommand=barra_rolagem_x.set, yscrollcommand=barra_rolagem_v.set)
        
        barra_rolagem_x.pack(side="bottom", fill="x")
        barra_rolagem_v.pack(side="right", fill="y")
        
        barra_rolagem_x.config(command=self.tabela.xview)
        barra_rolagem_v.config(command=self.tabela.yview)

        # Cabeçalhos da Tabela
        self.tabela.heading("matricula", text="Nº Matrícula")
        self.tabela.heading("nome", text="Nome Completo")
        self.tabela.heading("nome_pai", text="Nome do Pai")
        self.tabela.heading("disciplina", text="Disciplina")
        self.tabela.heading("nota", text="Menção/Nota")
        
        self.tabela["show"] = "headings"
        self.tabela.pack(fill="both", expand=1)

    # --- Operação: ADICIONAR ---
    def funcao_quadro_adicionar(self):
        self.quadro_cad_estudante = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(150, 180, 255))
        self.quadro_cad_estudante.place(x=(self.largura//3)+80, y=100, width=self.largura//3, height=self.altura-220)

        # Campos de Entrada (Labels e Entries)
        tk.Label(self.quadro_cad_estudante, text="Matrícula:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=25)
        self.var_matricula = tk.Entry(self.quadro_cad_estudante, width=18, font=("arial", 15, "bold"), bd=3)
        self.var_matricula.grid(row=0, column=1, padx=10, pady=25)

        tk.Label(self.quadro_cad_estudante, text="Nome:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=25)
        self.var_nome = tk.Entry(self.quadro_cad_estudante, width=18, font=("arial", 15, "bold"), bd=3)
        self.var_nome.grid(row=1, column=1, padx=10, pady=25)

        tk.Label(self.quadro_cad_estudante, text="Nome do Pai:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=2, column=0, padx=20, pady=25)
        self.var_nome_pai = tk.Entry(self.quadro_cad_estudante, width=18, font=("arial", 15, "bold"), bd=3)
        self.var_nome_pai.grid(row=2, column=1, padx=10, pady=25)

        tk.Label(self.quadro_cad_estudante, text="Disciplina:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=3, column=0, padx=20, pady=25)
        self.var_disciplina = tk.Entry(self.quadro_cad_estudante, width=18, font=("arial", 15, "bold"), bd=3)
        self.var_disciplina.grid(row=3, column=1, padx=10, pady=25)

        tk.Label(self.quadro_cad_estudante, text="Nota/Menção:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=4, column=0, padx=20, pady=25)
        self.var_nota = tk.Entry(self.quadro_cad_estudante, width=18, font=("arial", 15, "bold"), bd=3)
        self.var_nota.grid(row=4, column=1, padx=10, pady=25)

        btn_confirmar = tk.Button(self.quadro_cad_estudante, text="Cadastrar", width=20, font=("arial", 20, "bold"), command=self.funcao_cadastrar)
        btn_confirmar.grid(row=5, column=0, columnspan=2, pady=25)

    def funcao_cadastrar(self):
        if self.var_matricula.get()=="" or self.var_nome.get()=="":
            messagebox.showerror("Campos Vazios", "Por favor, preencha todos os campos obrigatórios")
        else:
            try:
                self.funcao_banco_dados()
                comando_sql = "insert into estudante values(%s,%s,%s,%s,%s)"
                self.cursor.execute(comando_sql, (self.var_matricula.get(), self.var_nome.get(), self.var_nome_pai.get(), self.var_disciplina.get(), self.var_nota.get()))
                self.conexao.commit()
                messagebox.showinfo("Sucesso", f"O estudante {self.var_nome.get()} foi registrado com sucesso!")
                self.conexao.close()
                self.quadro_cad_estudante.destroy()
                self.mostrar_todos()
            except Exception as e:
                messagebox.showerror("Erro SQL", f"Erro ao inserir dados: {e}")

    # --- Operação: BUSCA ---
    def funcao_quadro_busca(self):
        self.quadro_busca_f = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(150, 180, 255))
        self.quadro_busca_f.place(x=(self.largura//3)+80, y=100, width=self.largura//3, height=350)

        tk.Label(self.quadro_busca_f, text="Filtrar por:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=30)
        self.busca_opcao = ttk.Combobox(self.quadro_busca_f, width=17, font=("arial", 15, "bold"), state="readonly")
        self.busca_opcao['values'] = ("matricula", "nome", "disciplina")
        self.busca_opcao.grid(row=0, column=1, padx=10, pady=30)
        self.busca_opcao.set("Selecione Opção")

        tk.Label(self.quadro_busca_f, text="Valor da Busca:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=30)
        self.busca_valor = tk.Entry(self.quadro_busca_f, width=18, font=("arial", 15, "bold"), bd=3)
        self.busca_valor.grid(row=1, column=1, padx=10, pady=30)

        btn_pesquisar = tk.Button(self.quadro_busca_f, text="Pesquisar", width=20, font=("arial", 20, "bold"), command=self.funcao_pesquisar)
        btn_pesquisar.grid(row=2, column=0, columnspan=2, pady=30)

    def funcao_pesquisar(self):
        try:
            self.funcao_banco_dados()
            comando_sql = f"select * from estudante where {self.busca_opcao.get()} = %s"
            self.cursor.execute(comando_sql, (self.busca_valor.get()))
            linhas = self.cursor.fetchall()
            if len(linhas)!=0:
                self.tabela.delete(*self.tabela.get_children())
                for linha in linhas:
                    self.tabela.insert('', tk.END, values=linha)
                self.conexao.close()
            self.quadro_busca_f.destroy()
        except Exception as e:
            messagebox.showerror("Erro de Busca", f"Erro ao pesquisar estudante: {e}")

    # --- Operação: LISTAR TODOS ---
    def mostrar_todos(self):
        try:
            self.funcao_banco_dados()
            self.cursor.execute("select * from estudante")
            linhas = self.cursor.fetchall()
            self.tabela.delete(*self.tabela.get_children())
            for linha in linhas:
                self.tabela.insert('', tk.END, values=linha)
            self.conexao.close()
        except Exception as e:
            messagebox.showerror("Erro de Visualização", f"Erro ao listar estudantes: {e}")

    # --- Operação: ATUALIZAR ---
    def funcao_quadro_atualizar(self):
        self.quadro_atua_f = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(150, 180, 255))
        self.quadro_atua_f.place(x=(self.largura//3)+80, y=100, width=self.largura//3, height=350)

        tk.Label(self.quadro_atua_f, text="Campo a mudar:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=20)
        self.atua_opcao = ttk.Combobox(self.quadro_atua_f, width=17, font=("arial", 15, "bold"), state="readonly")
        self.atua_opcao['values'] = ("nome", "disciplina", "nota")
        self.atua_opcao.grid(row=0, column=1, padx=10, pady=20)

        tk.Label(self.quadro_atua_f, text="Novo Valor:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=20)
        self.atua_valor = tk.Entry(self.quadro_atua_f, width=18, font=("arial", 15, "bold"), bd=3)
        self.atua_valor.grid(row=1, column=1, padx=10, pady=20)

        tk.Label(self.quadro_atua_f, text="Nº Matrícula:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=2, column=0, padx=20, pady=20)
        self.atua_matricula = tk.Entry(self.quadro_atua_f, width=18, font=("arial", 15, "bold"), bd=3)
        self.atua_matricula.grid(row=2, column=1, padx=10, pady=20)

        btn_atualizar = tk.Button(self.quadro_atua_f, text="Atualizar", width=20, font=("arial", 20, "bold"), command=self.funcao_atualizar_registro)
        btn_atualizar.grid(row=3, column=0, columnspan=2, pady=20)

    def funcao_atualizar_registro(self):
        try:
            self.funcao_banco_dados()
            comando_sql = f"update estudante set {self.atua_opcao.get()} = %s where matricula = %s"
            self.cursor.execute(comando_sql, (self.atua_valor.get(), self.atua_matricula.get()))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
            self.conexao.close()
            self.quadro_atua_f.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro de Atualização", f"Erro ao atualizar registro: {e}")

    # --- Operação: EXCLUIR ---
    def funcao_quadro_remover(self):
        self.quadro_rem_f = tk.Frame(self.root, bd=5, relief="raised", bg=self.cor_rgb(150, 180, 255))
        self.quadro_rem_f.place(x=(self.largura//3)+80, y=100, width=self.largura//3, height=250)

        tk.Label(self.quadro_rem_f, text="Nº Matrícula:", bg=self.cor_rgb(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=30)
        self.rem_matricula = tk.Entry(self.quadro_rem_f, width=18, font=("arial", 15, "bold"), bd=3)
        self.rem_matricula.grid(row=0, column=1, padx=10, pady=30)

        btn_excluir = tk.Button(self.quadro_rem_f, text="Excluir", width=20, font=("arial", 20, "bold"), command=self.funcao_remover_registro)
        btn_excluir.grid(row=1, column=0, columnspan=2, pady=30)

    def funcao_remover_registro(self):
        try:
            self.funcao_banco_dados()
            comando_sql = "delete from estudante where matricula = %s"
            self.cursor.execute(comando_sql, (self.rem_matricula.get()))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", f"Estudante de matrícula {self.rem_matricula.get()} foi removido.")
            self.conexao.close()
            self.quadro_rem_f.destroy()
            self.mostrar_todos()
        except Exception as e:
            messagebox.showerror("Erro de Exclusão", f"Erro ao remover estudante: {e}")

if __name__ == "__main__":
    janela = tk.Tk()
    aplicativo = Estudante(janela)
    janela.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql


class std():
    def __init__(self,root):
        self.root = root
        self.root.title("Banco de Dados de Alunos")
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Banco de Dados de Alunos", bd=4, relief="raised", bg="lightgreen", font=("Elephant", 40, "bold"))
        title.pack(side="top", fill="x")

        optFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(230, 150, 200))
        optFrame.place(width=self.width/3, height=self.height-180, x=50, y=100)

        addBtn = tk.Button(optFrame,command= self.addFrameFun, text="Adicionar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        addBtn.grid(row=0, column=0, padx=30, pady=25)

        srchBtn = tk.Button(optFrame, text="Buscar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        srchBtn.grid(row=1, column=0, padx=30, pady=25)    

        updBtn = tk.Button(optFrame, text="Atualizar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        updBtn.grid(row=2, column=0, padx=30, pady=25)

        allBtn = tk.Button(optFrame, text="Mostrar Todos os Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        allBtn.grid(row=3, column=0, padx=30, pady=25)

        delBtn = tk.Button(optFrame, text="Remover Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        delBtn.grid(row=4, column=0, padx=30, pady=25)

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150, 230, 120))
        self.detFrame.place(width=self.width/2+50, height=self.height-180, x=self.width/3+100, y=100)

        lbl = tk.Label(self.detFrame, text="Detalhes do Aluno", font=("Arial", 30, "bold"))
        lbl.pack(side="top", fill="x")

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2, height=self.height-280, x=23, y=80)

        x_scroll = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = tk.Scrollbar(tabFrame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, columns=("numero", "name", "mnome", "turno", "turma"))

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        
        self.table.heading("numero", text="Id do Aluno")
        self.table.heading("name", text="Nome")
        self.table.heading("mnome", text="Nome da Mãe")
        self.table.heading("turno", text="Turno")
        self.table.heading("turma", text="Turma")
        self.table["show"] = "headings"

        self.table.pack(fill="both", expand=1)

    def addFrameFun(self):
        self.addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150, 180, 250))
        self.addFrame.place(width=self.width/3, height=self.height-180, x=self.width/3+80, y=100)

        numero = tk.Label(self.addFrame, text="Id do Aluno:", bg=self.clr(150, 180, 250), font=("arial", 15, "bold"))
        numero.grid(row=0, column=0, padx=20, pady=30)
        self.numero = tk.Entry(self.addFrame, width=18, font=("arial", 15, "bold"), bd=3)
        self.numero.grid(row=0, column=1, padx=10, pady=30)

        name = tk.Label(self.addFrame, text="Nome:", bg=self.clr(150, 180, 250), font=("arial", 15, "bold"))
        name.grid(row=1, column=0, padx=20, pady=30)
        self.name = tk.Entry(self.addFrame, width=18, font=("arial", 15, "bold"), bd=3)
        self.name.grid(row=1, column=1, padx=10, pady=30)

        mnome = tk.Label(self.addFrame, text="Nome da Mãe:", bg=self.clr(150, 180, 250), font=("arial", 15, "bold"))
        mnome.grid(row=2, column=0, padx=20, pady=30)
        self.mnome = tk.Entry(self.addFrame, width=18, font=("arial", 15, "bold"), bd=3)
        self.mnome.grid(row=2, column=1, padx=10, pady=30)

        turno = tk.Label(self.addFrame, text="Turno:", bg=self.clr(150, 180, 250), font=("arial", 15, "bold"))
        turno.grid(row=3, column=0, padx=20, pady=30)
        self.turno = tk.Entry(self.addFrame, width=18, font=("arial", 15, "bold"), bd=3)
        self.turno.grid(row=3, column=1, padx=10, pady=30)

        turma = tk.Label(self.addFrame, text="Turma:", bg=self.clr(150, 180, 250), font=("arial", 15, "bold"))
        turma.grid(row=4, column=0, padx=20, pady=30)
        self.turma = tk.Entry(self.addFrame, width=18, font=("arial", 15, "bold"), bd=3)
        self.turma.grid(row=4, column=1, padx=10, pady=30)

        okBtn = tk.Button(self.addFrame, command=self.addFun, text="Enter", bd=3, relief="raised", font=("Arial", 20, "bold"), width=20)
        okBtn.grid(row=5, column=0, padx=30, pady=25, columnspan=2)

    def desAdd(self):
        self.addFrame.destroy()

    def addFun(self):
        id_val = self.numero.get()
        name = self.name.get()
        mnome = self.mnome.get()
        turno = self.turno.get()
        turma = self.turma.get()

        if id_val and name and mnome and turno and turma:
            numero = int(id_val)
            try: 
                self.dbFun()
                sql_insert = "INSERT INTO aluno (numero, name, mnome, turno, turma) VALUES (%s, %s, %s, %s, %s)"
                valores = (numero, name, mnome, turno, turma)
            
                self.cur.execute(sql_insert, valores)
                self.con.commit()
                tk.messagebox.showinfo("Sucesso", f"Estudante {name} com o numero {numero} está registrado.")

                self.cur.execute("SELECT * FROM aluno WHERE numero=%s", (numero,))
                row = self.cur.fetchone()
            if row:

                self.table.delete(*self.table.get_children())
                self.table.insert('', tk.END, values=row)

                self.con.close()

            except Exception as e: 
            tk.messagebox.showerror("Erro", f"Error: {e}")
            self.desAdd()
        else: 
            tk.messagebox.showerror("Erro", "Por Favor, preencha todos os espaços indicado")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", password="", database="aluno")
        self.cur = self.con.cursor()

    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
root = tk.Tk()
obj = std(root)
root.mainloop()

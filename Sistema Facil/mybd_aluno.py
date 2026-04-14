import tkinter as tk
from tkinter import ttk

class std():
    def __init__(self,root):
        self.root = root
        self.root.tittle("Banco de Dados de Alunos")
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Banco de Dados de Alunos", bd=4, relief="raised", bg="lightgreen", font=("Elephant", 40, "bold"))
        title.pack(side="top", fill="x")

        optFrame = tk.Frame(self.root, bd=5, relief="rigde", bg=self.clr(230, 150, 200))
        optFrame.place(width=self.width/3, height=self.height-180, x=50, y=100)

        addBtn = tk.Button(optFrame, text="Adicionar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        addBtn.grid(row=0, column=0, padx=30, pady=25)

        srchBtn = tk.Button(optFrame, text="Buscar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        srchBtn.grid(row=1, column=0, padx=30, pady=25)    

        updBtn = tk.Button(optFrame, text="Atualizar Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        updBtn.grid(row=2, column=0, padx=30, pady=25)

        allBtn = tk.Button(optFrame, text="Mostrar Todos os Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        allBtn.grid(row=3, column=0, padx=30, pady=25)

        delBtn = tk.Button(optFrame, text="Remover Aluno", bd=3, relief="raised", bg="lightgrey", width=20, font=("Arial", 20, "bold"))
        delBtn.grid(row=4, column=0, padx=30, pady=25)

        self.detFrame = tk.Frame(self.rot, bd=5, relief="rigde", bg=self.clr(150, 230, 120))
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

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, columns=("roll", "name", "fname", "sub", "grade"))

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        
        self.table.heading("roll", text="Roll_No")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father_Name")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="Grade")
        self.table["show"] = "headings"




        self.table.pacl(fill="both", expand=1)
    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
root = tk.TK()
obj = std(root)
root.mainloop()

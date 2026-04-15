import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record")
        
        # Variáveis globais para dimensões da tela
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        # Título principal
        title = tk.Label(self.root, text="Student Record Management System", bd=4, relief="raised", 
                         bg="lightgreen", font=("elephant", 40, "bold"))
        title.pack(side="top", fill="x")

        # Função auxiliar para gerar cores hexadecimais
        def color(self, r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'

        # Frame de Opções (Esquerda)
        self.opt_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(230, 150, 200))
        self.opt_frame.place(x=50, y=100, width=self.width//3, height=self.height-180)

        # Botões do Frame de Opções
        add_btn = tk.Button(self.opt_frame, text="Add Student", bd=3, relief="raised", bg="lightgrey",
                            width=20, font=("arial", 15, "bold"), command=self.add_frame_function)
        add_btn.grid(row=0, column=0, padx=30, pady=25)

        search_btn = tk.Button(self.opt_frame, text="Search Student", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.search_frame_function)
        search_btn.grid(row=1, column=0, padx=30, pady=25)

        update_btn = tk.Button(self.opt_frame, text="Update Record", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.update_frame_function)
        update_btn.grid(row=2, column=0, padx=30, pady=25)

        show_all_btn = tk.Button(self.opt_frame, text="Show All", bd=3, relief="raised", bg="lightgrey",
                                 width=20, font=("arial", 15, "bold"), command=self.show_all)
        show_all_btn.grid(row=3, column=0, padx=30, pady=25)

        delete_btn = tk.Button(self.opt_frame, text="Remove Student", bd=3, relief="raised", bg="lightgrey",
                               width=20, font=("arial", 15, "bold"), command=self.del_frame_function)
        delete_btn.grid(row=4, column=0, padx=30, pady=25)

        # Frame de Detalhes (Direita)
        self.detail_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(150, 230, 120))
        self.detail_frame.place(x=(self.width//3)+100, y=100, width=(self.width//2)+50, height=self.height-180)

        lbl_detail = tk.Label(self.detail_frame, text="Record Details", font=("arial", 30, "bold"), 
                              bg=self.color(150, 230, 120))
        lbl_detail.pack(side="top", fill="x")

        # Chamada da função da tabela
        self.tab_function()

    def color(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def db_function(self):
        try:
            self.con = pymysql.connect(host="localhost", user="root", password="SUA_PASSWORD", database="record")
            self.cursor = self.con.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def tab_function(self):
        self.tab_frame = tk.Frame(self.detail_frame, bd=4, relief="sunken", bg="cyan")
        self.tab_frame.place(x=23, y=70, width=(self.width//2), height=self.height-280)

        x_scroll = tk.Scrollbar(self.tab_frame, orient="horizontal")
        v_scroll = tk.Scrollbar(self.tab_frame, orient="vertical")

        self.table = ttk.Treeview(self.tab_frame, columns=("roll", "name", "fname", "sub", "grade"),
                                  xscrollcommand=x_scroll.set, yscrollcommand=v_scroll.set)
        
        x_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        
        x_scroll.config(command=self.table.xview)
        v_scroll.config(command=self.table.yview)

        self.table.heading("roll", text="Roll Number")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father Name")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="Grade")
        
        self.table["show"] = "headings"
        self.table.pack(fill="both", expand=1)

    # --- Funções para Adicionar ---
    def add_frame_function(self):
        self.add_f_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(150, 180, 255))
        self.add_f_frame.place(x=(self.width//3)+80, y=100, width=self.width//3, height=self.height-220)

        # Labels e Entries para cadastro
        tk.Label(self.add_f_frame, text="Roll Number:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=25)
        self.roll_no_var = tk.Entry(self.add_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.roll_no_var.grid(row=0, column=1, padx=10, pady=25)

        tk.Label(self.add_f_frame, text="Name:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=25)
        self.name_var = tk.Entry(self.add_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.name_var.grid(row=1, column=1, padx=10, pady=25)

        tk.Label(self.add_f_frame, text="Father Name:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=2, column=0, padx=20, pady=25)
        self.fname_var = tk.Entry(self.add_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.fname_var.grid(row=2, column=1, padx=10, pady=25)

        tk.Label(self.add_f_frame, text="Subject:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=3, column=0, padx=20, pady=25)
        self.subject_var = tk.Entry(self.add_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.subject_var.grid(row=3, column=1, padx=10, pady=25)

        tk.Label(self.add_f_frame, text="Grade:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=4, column=0, padx=20, pady=25)
        self.grade_var = tk.Entry(self.add_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.grade_var.grid(row=4, column=1, padx=10, pady=25)

        enter_btn = tk.Button(self.add_f_frame, text="Enter", width=20, font=("arial", 20, "bold"), command=self.add_function)
        enter_btn.grid(row=5, column=0, columnspan=2, pady=25)

    def add_function(self):
        if self.roll_no_var.get()=="" or self.name_var.get()=="":
            messagebox.showerror("Error", "Please fill all input fields")
        else:
            try:
                self.db_function()
                query = "insert into student values(%s,%s,%s,%s,%s)"
                self.cursor.execute(query, (self.roll_no_var.get(), self.name_var.get(), self.fname_var.get(), self.subject_var.get(), self.grade_var.get()))
                self.con.commit()
                messagebox.showinfo("Success", f"Student {self.name_var.get()} registered successfully")
                self.con.close()
                self.add_f_frame.destroy()
                self.show_all()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    # --- Funções para Busca ---
    def search_frame_function(self):
        self.search_f_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(150, 180, 255))
        self.search_f_frame.place(x=(self.width//3)+80, y=100, width=self.width//3, height=350)

        tk.Label(self.search_f_frame, text="Select Option:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=30)
        self.search_opt = ttk.Combobox(self.search_f_frame, width=17, font=("arial", 15, "bold"), state="readonly")
        self.search_opt['values'] = ("roll_number", "name", "sub")
        self.search_opt.grid(row=0, column=1, padx=10, pady=30)
        self.search_opt.set("Select Option")

        tk.Label(self.search_f_frame, text="Enter Value:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=30)
        self.search_val = tk.Entry(self.search_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.search_val.grid(row=1, column=1, padx=10, pady=30)

        search_btn = tk.Button(self.search_f_frame, text="Search", width=20, font=("arial", 20, "bold"), command=self.search_function)
        search_btn.grid(row=2, column=0, columnspan=2, pady=30)

    def search_function(self):
        try:
            self.db_function()
            query = f"select * from student where {self.search_opt.get()} = %s"
            self.cursor.execute(query, (self.search_val.get()))
            rows = self.cursor.fetchall()
            if len(rows)!=0:
                self.table.delete(*self.table.get_children())
                for row in rows:
                    self.table.insert('', tk.END, values=row)
                self.con.close()
            self.search_f_frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # --- Função Mostrar Todos ---
    def show_all(self):
        try:
            self.db_function()
            self.cursor.execute("select * from student")
            rows = self.cursor.fetchall()
            self.table.delete(*self.table.get_children())
            for row in rows:
                self.table.insert('', tk.END, values=row)
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # --- Funções para Atualizar ---
    def update_frame_function(self):
        self.upd_f_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(150, 180, 255))
        self.upd_f_frame.place(x=(self.width//3)+80, y=100, width=self.width//3, height=350)

        tk.Label(self.upd_f_frame, text="Select Field:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=20)
        self.upd_opt = ttk.Combobox(self.upd_f_frame, width=17, font=("arial", 15, "bold"), state="readonly")
        self.upd_opt['values'] = ("name", "sub", "grade")
        self.upd_opt.grid(row=0, column=1, padx=10, pady=20)

        tk.Label(self.upd_f_frame, text="New Value:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=1, column=0, padx=20, pady=20)
        self.upd_val = tk.Entry(self.upd_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.upd_val.grid(row=1, column=1, padx=10, pady=20)

        tk.Label(self.upd_f_frame, text="Roll Number:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=2, column=0, padx=20, pady=20)
        self.upd_roll = tk.Entry(self.upd_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.upd_roll.grid(row=2, column=1, padx=10, pady=20)

        upd_btn = tk.Button(self.upd_f_frame, text="Update", width=20, font=("arial", 20, "bold"), command=self.update_function)
        upd_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def update_function(self):
        try:
            self.db_function()
            query = f"update student set {self.upd_opt.get()} = %s where roll_number = %s"
            self.cursor.execute(query, (self.upd_val.get(), self.upd_roll.get()))
            self.con.commit()
            messagebox.showinfo("Success", "Record Updated Successfully")
            self.con.close()
            self.upd_f_frame.destroy()
            self.show_all()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # --- Funções para Remover ---
    def del_frame_function(self):
        self.del_f_frame = tk.Frame(self.root, bd=5, relief="raised", bg=self.color(150, 180, 255))
        self.del_f_frame.place(x=(self.width//3)+80, y=100, width=self.width//3, height=250)

        tk.Label(self.del_f_frame, text="Roll Number:", bg=self.color(150, 180, 255), font=("arial", 15, "bold")).grid(row=0, column=0, padx=20, pady=30)
        self.del_roll = tk.Entry(self.del_f_frame, width=18, font=("arial", 15, "bold"), bd=3)
        self.del_roll.grid(row=0, column=1, padx=10, pady=30)

        del_btn = tk.Button(self.del_f_frame, text="Delete", width=20, font=("arial", 20, "bold"), command=self.delete_function)
        del_btn.grid(row=1, column=0, columnspan=2, pady=30)

    def delete_function(self):
        try:
            self.db_function()
            query = "delete from student where roll_number = %s"
            self.cursor.execute(query, (self.del_roll.get()))
            self.con.commit()
            messagebox.showinfo("Success", f"Student with Roll {self.del_roll.get()} removed")
            self.con.close()
            self.del_f_frame.destroy()
            self.show_all()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    obj = Student(root)
    root.mainloop()

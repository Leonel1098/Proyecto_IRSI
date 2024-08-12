from tkinter import Tk
import tkinter as tk
from tkinter import Frame
from tkinter import Button, filedialog,Label

class Prestamos:

    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        #self.libros_dic = {}

        
    # Estructura y componentes de la ventana de Prestamos
    def ventana_Prestamo(self):
        self.ventana_principal.iconify()
        self.ventana_prestamos = tk.Toplevel()
        self.ventana_prestamos.title("Gestionando Prestamos")
        self.ventana_prestamos.geometry("%dx%d+%d+%d" % (500, 300, 450, 220))
        self.ventana_prestamos.resizable(0, 0)

        prestamos_Frame = Frame(self.ventana_prestamos)
        prestamos_Frame.pack(side="top")
        prestamos_Frame.place(width="500", height="300")
        prestamos_Frame.config(bg="black")

        label_isbn = Label(prestamos_Frame, text="Ingrese el ISBN del libro", font=("Modern", 12), foreground="white")
        label_isbn.pack()
        label_isbn.config(bg="black")
        label_isbn.place(x=20, y=50, width=200, height=20)

        entrada_isbn = tk.Entry(prestamos_Frame)
        entrada_isbn.pack()
        entrada_isbn.place(x=200, y=50, width=160, height=20)

        label_id_usuario = Label(prestamos_Frame, text="Ingrese el ID del Usuario", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=90, width=200, height=20)

        entrada_id_usuario = tk.Entry(prestamos_Frame)
        entrada_id_usuario.pack()
        entrada_id_usuario.place(x=200, y=90, width=160, height=20)

        button_prestar = Button(prestamos_Frame, text="Prestar Libro", font=("Modern", 12), foreground="white", highlightthickness=2)
        button_prestar.pack()
        button_prestar.config(bg="black")
        button_prestar.place(x=180, y=140, width=110, height=20)

        button_devolver = Button(prestamos_Frame, text="Devolver Libro", font=("Modern", 12), foreground="white", highlightthickness=2)
        button_devolver.pack()
        button_devolver.config(bg="black")
        button_devolver.place(x=300, y=140, width=110, height=20)

        button_regresar = Button(prestamos_Frame, text="Regresar", command= lambda: self.regresar(self.ventana_prestamos), font=("Modern", 12), foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=370, y=265, width=110, height=20)

    def regresar(self, ventana):
        ventana.destroy()
        self.ventana_principal.deiconify()
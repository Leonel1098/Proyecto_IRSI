from tkinter import Tk
import tkinter as tk
from tkinter import Frame
from tkinter import Button, filedialog,Label

class Morosidad:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        #self.libros_dic = {}
    # Estructura y componentes de la ventana de Morosidad
    def ventana_Morosidad(self):
        self.ventana_principal.iconify()
        self.ventana_morosidad = tk.Toplevel()
        self.ventana_morosidad.title("Gestionando Usuarios")
        self.ventana_morosidad.geometry("%dx%d+%d+%d" % (500, 300, 450, 220))
        self.ventana_morosidad.resizable(0, 0)

        morosidad_Frame = Frame(self.ventana_morosidad)
        morosidad_Frame.pack(side="top")
        morosidad_Frame.place(width="500", height="300")
        morosidad_Frame.config(bg="black")

        label_isbn = Label(morosidad_Frame, text="Ingrese el ISBN del libro", font=("Modern", 12), foreground="white")
        label_isbn.pack()
        label_isbn.config(bg="black")
        label_isbn.place(x=20, y=50, width=200, height=20)

        entrada_isbn = tk.Entry(morosidad_Frame)
        entrada_isbn.pack()
        entrada_isbn.place(x=200, y=50, width=160, height=20)

        label_id_usuario = Label(morosidad_Frame, text="Ingrese el ID del Usuario", font=("Modern", 12),foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=90, width=200, height=20)

        entrada_id_usuario = tk.Entry(morosidad_Frame)
        entrada_id_usuario.pack()
        entrada_id_usuario.place(x=200, y=90, width=160, height=20)

        button_morosidad = Button(morosidad_Frame, text="Consultar la morosidad", font=("Modern", 12), foreground="white",highlightthickness=2)
        button_morosidad.pack()
        button_morosidad.config(bg="black")
        button_morosidad.place(x=120, y=140, width=160, height=20)

        button_devolver_morosidad = Button(morosidad_Frame, text="Devolver Libro con Morosidad", font=("Modern", 12), foreground="white",highlightthickness=2)
        button_devolver_morosidad.pack()
        button_devolver_morosidad.config(bg="black")
        button_devolver_morosidad.place(x=290, y=140, width=180, height=20)

        button_regresar = Button(morosidad_Frame, text="Regresar",command=lambda: self.regresar(self.ventana_morosidad), font=("Modern", 12),foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=370, y=265, width=110, height=20)
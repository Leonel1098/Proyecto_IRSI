#Importaciones de las librerias
from tkinter import Tk
import tkinter as tk
from tkinter import Frame
from tkinter import Button, filedialog,Label

#Importando las otras clases 
from Libros import Libros 
from Usuarios import Usuarios
from Morosidad import Morosidad
from Prestamos import Prestamos


class Interfaz:
    
    """#Varibles que contienen los metodos de las ventanas de las otras clases
    ventana_libros = Libros.ventana_Libros
    guardar_libros = Libros.guardar_libros
    cargar_libros = Libros.cargar_libros
    eliminar_libro = Libros.eliminar_libro
    actualizar_combobox = Libros.actualizar_combobox
    ventana_prestamos = Prestamos.ventana_Prestamo
    ventana_morosidad = Morosidad.ventana_Morosidad
    ventana_usuarios = Usuarios.ventana_Usuarios"""

    #Metodo constructor, inicializa la ventana principal y crea las instancias de las otras clases para trabajar con sus metodos
    def __init__(self, root):
        # Inicializar la ventana principal
        self.ventana_principal = root
        # Crear instancias de las otras clases
        self.libros = Libros(self.ventana_principal)
        self.usuarios = Usuarios(self.ventana_principal)
        self.morosidad = Morosidad(self.ventana_principal)
        self.prestamos = Prestamos(self.ventana_principal)
        
        # lama al metodo que contiene toda la configuracion de la ventana principal del programa
        self.ventana_Principal()

    #Estructura y componentes de la Ventana principal del Programa
    def ventana_Principal(self):
        #Configuracion de la ventana principal
        self.ventana_principal.title("Gestion de Biblioteca")
        self.ventana_principal.geometry("%dx%d+%d+%d" % (700,500,360,120))
        self.ventana_principal.resizable(0,0)

        #Se agrega un frame a la ventan principal que contendra todos los widgets 
        p_Frame = Frame(self.ventana_principal)
        p_Frame.pack(side = "top")
        p_Frame.place(width= "900", height ="500")
        p_Frame.config(bg = "black")

        label_titulo = Label(p_Frame, text = "Gestion de Biblioteca",font=("Modern", 28), foreground= "white")
        label_titulo.pack()
        label_titulo.config(bg= "black")
        label_titulo.place(x = 200, y = 110 , width= 300, height= 50)

        button_libros = Button(p_Frame, text="Libros", command= self.abrir_ventana_libros,font=("Modern", 16), foreground = "white", highlightthickness=2)
        button_libros.pack()
        button_libros.config(bg = "black")
        button_libros.place(x = 95,y = 250,width= 100, height  = 40)


        button_usuarios = Button(p_Frame, text="Usuarios", command=self.abrir_ventana_usuarios,font=("Modern", 16), foreground = "white", highlightthickness=2)
        button_usuarios.pack()
        button_usuarios.config(bg = "black")
        button_usuarios.place(x = 195,y = 250, width= 100, height  = 40 )

        button_prestamo = Button(p_Frame, text="Prestamos",font=("Modern", 16), command= self.abrir_ventana_prestamos, foreground = "white", highlightthickness=2)
        button_prestamo.pack()
        button_prestamo.config(bg = "black")
        button_prestamo.place(x =295,y= 250, width= 100, height  = 40)

        button_utilidades = Button(p_Frame, text="Abrir Archivo",font=("Modern", 16), foreground = "white", highlightthickness=2)
        button_utilidades.pack()
        button_utilidades.config(bg = "black")
        button_utilidades.place(x =395, y = 250, width= 120, height  = 40)

        button_morosidad = Button(p_Frame, text="Morosidad", command= self.abrir_ventana_morosidad,font=("Modern", 16), foreground = "white", highlightthickness=2)
        button_morosidad.pack()
        button_morosidad.config(bg = "black")
        button_morosidad.place(x =510, y = 250, width= 100, height  = 40)
        self.ventana_principal.mainloop()

    #Estos metodos llaman a las intancias de las clases creadas, se usan para que los botones abran 
    # las ventanas de las demas funcionalidades del programa.

    def abrir_ventana_libros(self):
        self.libros.ventana_Libros()

    def abrir_ventana_usuarios(self):
        self.usuarios.ventana_Usuarios()

    def abrir_ventana_prestamos(self):
        self.prestamos.ventana_Prestamo()

    def abrir_ventana_morosidad(self):
        self.morosidad.ventana_Morosidad()

    #Este metodo sirve para ocultar la ventana en la que se trabaja al regresar a la ventana principal
    def regresar(self, ventana):
        self.ventana_principal.deiconify()
        ventana.destroy()

if __name__ == "__main__":
    root = Tk()
    app = Interfaz(root)
    root.mainloop()
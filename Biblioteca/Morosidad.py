from tkinter import Tk
import datetime
import tkinter as tk
from tkinter import Frame
from tkinter import Button, filedialog,Label,messagebox

class Morosidad:
    #Metodo constructor que crea la instancia con la ventana principal
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.Data_Prestamos_Registro = "Biblioteca/Registro_Prestamos.txt"
        self.Data_Devoluciones = "Biblioteca/Devoluciones.txt"
        self.dias_limite = 7 
        self.mora_diaria = 3  

    #En este metodo hacemos el procedimiento para calcular la mora de los prestamos realizados por los usuarios, 
    # usando los datos obtenidos de los archivos txt creados en prestamos 
    def calcular_morosidad(self):
        isbn = self.entrada_isbn.get()
        usuario_id = self.entrada_id_usuario.get()
        fecha_prestamo = None
        fecha_devolucion = None
        
        try:
            #En esta parte cargamos el archivo de prestamos y realizamos la busqueda de la fecha para agregarla a la fecha prestamo
            with open(self.Data_Prestamos_Registro, 'r') as archivo:
                prestamos = archivo.readlines()
                for prestamo in prestamos:
                    if f"Codigo ISBN: {isbn}, ID Usuario: {usuario_id}" in prestamo:
                        partes = prestamo.split(", ")
                        fecha_prestamo = datetime.datetime.strptime(partes[2].split(": ")[1].strip(), '%Y-%m-%d')
                        break
        except FileNotFoundError:
            messagebox.showerror(title="Error Prestamo", message="Archivo de préstamos no encontrado.")
            return

        ##En esta parte cargamos el archivo de devoluciones y realizamos la busqueda de la fecha para agregarla a la fecha devolucion
        try:
            with open(self.Data_Devoluciones, 'r') as archivo:
                devoluciones = archivo.readlines()
                for devolucion in devoluciones:
                    if f"Codigo ISBN: {isbn}, ID Usuario: {usuario_id}" in devolucion:
                        partes = devolucion.split(", ")
                        fecha_devolucion = datetime.datetime.strptime(partes[2].split(": ")[1].strip(), '%Y-%m-%d')
                        break
        except FileNotFoundError:
            messagebox.showerror(title="Error Devolucion", message="Archivo de devoluciones no encontrado.")
            return
        
        #Aqui se verifica que existan las fechas en los archivos de prestamos y devoluciones, 
        # si no encuentran las fechas significa que el prestamo o la devolucion no se hizo
        if not fecha_prestamo:
            messagebox.showerror(title="Error Prestamo", message="No se encontró un préstamo para el ISBN y ID de usuario proporcionados.")
            return
        if not fecha_devolucion:
            messagebox.showerror(title="Error Devollucion", message="No se encontró una devolución para el ISBN y ID de usuario proporcionados.")
            return

        #Aqui calculamos el tiempo que tiene la devolucion de retraso 
        retraso = (fecha_devolucion - fecha_prestamo).days - self.dias_limite
        
        #En esta parte validamos el tiempo de retraso y le calculamos el valor a la mora.
        if retraso > 0:
            mora = retraso * self.mora_diaria
            messagebox.showinfo(title="Morasidad", message=f"La mora para el libro con ISBN {isbn} y ID Usuario {usuario_id} es de {mora} quetzales.")
        else:
            messagebox.showinfo(title="Morosidad", message=f"No hay mora para el libro con ISBN {isbn} y ID Usuario {usuario_id}.")


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

        self.entrada_isbn = tk.Entry(morosidad_Frame)
        self.entrada_isbn.pack()
        self.entrada_isbn.place(x=200, y=50, width=160, height=20)

        label_id_usuario = Label(morosidad_Frame, text="Ingrese el ID del Usuario", font=("Modern", 12),foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=90, width=200, height=20)

        self.entrada_id_usuario = tk.Entry(morosidad_Frame)
        self.entrada_id_usuario.pack()
        self.entrada_id_usuario.place(x=200, y=90, width=160, height=20)

        button_morosidad = Button(morosidad_Frame, text="Consultar la morosidad",command= self.calcular_morosidad, font=("Modern", 12), foreground="white",highlightthickness=2)
        button_morosidad.pack()
        button_morosidad.config(bg="black")
        button_morosidad.place(x=200, y=140, width=160, height=20)

        """button_devolver_morosidad = Button(morosidad_Frame, text="Devolver Libro con Morosidad", font=("Modern", 12), foreground="white",highlightthickness=2)
        button_devolver_morosidad.pack()
        button_devolver_morosidad.config(bg="black")
        button_devolver_morosidad.place(x=290, y=140, width=180, height=20)"""

        button_regresar = Button(morosidad_Frame, text="Regresar",command=lambda: self.regresar(self.ventana_morosidad), font=("Modern", 12),foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=370, y=265, width=110, height=20)


    #Este metodo sirve para ocultar la ventana en la que se trabaja al regresar a la ventana principal
    def regresar(self, ventana):
        self.ventana_principal.deiconify()
        ventana.destroy()
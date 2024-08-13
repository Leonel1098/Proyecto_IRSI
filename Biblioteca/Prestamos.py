from tkinter import Tk,ttk
from tkcalendar import DateEntry
import tkinter as tk
import datetime
from tkinter import Frame
from tkinter import Button, filedialog,Label,messagebox
from Libros import Libros
from Usuarios import Usuarios
Data_Libros = "Biblioteca/Libros.txt"
Data_Prestamos = "Biblioteca/Prestamos.txt"
Data_User = "Biblioteca/Usuarios.txt"

class Prestamos:

    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.libros_dic = {}
        self.usuarios_dic = {}


    def cargar_libros(self):
        try:
            with open(Data_Libros, 'r') as archivo:
                for linea in archivo:
                    if "Codigo ISBN:" in linea:
                        partes = linea.split("Codigo ISBN:")
                        isbn = partes[1].strip()

                        # Obtiene el título y autor del libro
                        titulo_autor_partes = partes[0].split(", ")
                        if len(titulo_autor_partes) >= 2:
                            titulo = titulo_autor_partes[0].replace("Nombre del Libro: ", "").strip()
                            autor = titulo_autor_partes[1].replace("Autor: ", "").strip()
                            
                            # Actualiza el diccionario con los datos del libro
                            self.libros_dic[isbn] = {'titulo': titulo, 'autor': autor}
        except FileNotFoundError:
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_Libros} no esta creado aun")
        return self.libros_dic
    
    def cargar_usuarios(self):
        try:
            with open(Data_User, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea: 
                        continue
                    partes = linea.split(", ")
                    if len(partes) != 2:
                        print(f"Línea malformada detectada y omitida: {linea}")
                        continue
                    try:
                        nombre = partes[0].split(": ")[1]
                        usuario_id = partes[1].split(": ")[1]
                        self.usuarios_dic[usuario_id] = {'Nombre del Usuario': nombre, 'ID del Usuario': usuario_id}
                    except IndexError:
                        print(f"Línea malformada detectada y omitida: {linea}")
        except FileNotFoundError:
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_User} no está creado aún")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error al cargar el archivo: {e}")
        return self.usuarios_dic
    
    def configurar_combo_boxes(self, combobox_id_usuario, combobox_isbn):
        self.combobox_id_usuario = combobox_id_usuario
        self.combobox_isbn = combobox_isbn
        usuarios = self.cargar_usuarios()
        libros = self.cargar_libros()
        
        # Limpiar los ComboBox actuales
        self.combobox_id_usuario['values'] = list(usuarios.keys())
        self.combobox_isbn['values'] = list(libros.keys())
        
    def registrar_prestamo(self):
        usuario_id = self.combobox_id_usuario.get()
        libro_isbn = self.combobox_isbn.get()
        fecha_inicio = fecha_inicio_entry.get_date()
        
        if usuario_id and libro_isbn and fecha_inicio:
            try:
                with open(Data_Prestamos, 'a') as f:
                    f.write(f"{libro_isbn}, {usuario_id}, {fecha_inicio}\n")
                print(f"Préstamo registrado: {libro_isbn}, {usuario_id}, {fecha_inicio}")
            except Exception as e:
                print(f"Error al registrar el préstamo: {e}")
        else:
            print("Por favor, complete todos los campos.")


    def devolver_libro(self):
        usuario_id = self.combobox_id_usuario.get()
        libro_isbn = self.combobox_isbn.get()
        
        fecha_entrega = fecha_entrega_entry.get_date()
        
        if usuario_id and libro_isbn and fecha_entrega:
            try:
                # Leer los datos de los préstamos existentes
                prestamos = []
                with open('prestamos.txt', 'r') as f:
                    prestamos = f.readlines()
                
                with open('prestamos.txt', 'w') as f:
                    for prestamo in prestamos:
                        if prestamo.startswith(f"{libro_isbn}, {usuario_id},"):
                            f.write(f"{libro_isbn}, {usuario_id}, {fecha_entrega}\n")
                        else:
                            f.write(prestamo)
                
                print(f"Devolución registrada: {libro_isbn}, {usuario_id}, {fecha_entrega}")
            except Exception as e:
                print(f"Error al registrar la devolución: {e}")
        else:
            print("Por favor, complete todos los campos.")

    
    # Estructura y componentes de la ventana de Prestamos
    def ventana_Prestamo(self):
        self.ventana_principal.iconify()
        self.ventana_prestamos = tk.Toplevel()
        self.ventana_prestamos.title("Gestionando Prestamos")
        self.ventana_prestamos.geometry("%dx%d+%d+%d" % (550, 300, 450, 220))
        self.ventana_prestamos.resizable(0, 0)

        prestamos_Frame = Frame(self.ventana_prestamos)
        prestamos_Frame.pack(side="top")
        prestamos_Frame.place(width="550", height="300")
        prestamos_Frame.config(bg="black")

        label_isbn = Label(prestamos_Frame, text="Seleccione el ISBN del libro", font=("Modern", 12), foreground="white")
        label_isbn.pack()
        label_isbn.config(bg="black")
        label_isbn.place(x=20, y=50, width=180, height=20)

        combobox_isbn = ttk.Combobox(prestamos_Frame)
        combobox_isbn.pack()
        combobox_isbn.place(x=240, y=50, width=160, height=20)
        

        label_id_usuario = Label(prestamos_Frame, text="Seleccione el ID del Usuario", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=90, width=180, height=20)

        combobox_id_usuario = ttk.Combobox(prestamos_Frame)
        combobox_id_usuario.pack()
        combobox_id_usuario.place(x=240, y=90, width=160, height=20)

        self.configurar_combo_boxes(combobox_id_usuario,combobox_isbn)
        

        label_id_usuario = Label(prestamos_Frame, text="Seleccione la fecha del Prestamo", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=130, width=210, height=20)

        global fecha_inicio_entry
        fecha_inicio_entry = DateEntry(prestamos_Frame, date_pattern='yyyy-mm-dd')
        fecha_inicio_entry.pack()
        fecha_inicio_entry.place(x=240, y=130, width=160,height=20)

        label_id_usuario = Label(prestamos_Frame, text="Seleccione la fecha de Entrega", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=170, width=190, height=20)

        global fecha_entrega_entry
        fecha_entrega_entry = DateEntry(prestamos_Frame, date_pattern='yyyy-mm-dd')
        fecha_entrega_entry.pack()
        fecha_entrega_entry.place(x=240, y=170, width=160,height=20)

        button_prestar = Button(prestamos_Frame, text="Prestar Libro", command= self.registrar_prestamo, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_prestar.pack()
        button_prestar.config(bg="black")
        button_prestar.place(x=430, y=130, width=110, height=20)

        button_devolver = Button(prestamos_Frame, text="Devolver Libro", font=("Modern", 12), foreground="white", highlightthickness=2)
        button_devolver.pack()
        button_devolver.config(bg="black")
        button_devolver.place(x=430, y=170, width=110, height=20)

        button_regresar = Button(prestamos_Frame, text="Regresar", command= lambda: self.regresar(self.ventana_prestamos), font=("Modern", 12), foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=430, y=265, width=110, height=20)

    def regresar(self, ventana):
        ventana.destroy()
        self.ventana_principal.deiconify()
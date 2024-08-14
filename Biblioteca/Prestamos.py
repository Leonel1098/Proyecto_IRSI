#Importando librerias
from tkinter import Tk,ttk
from tkcalendar import DateEntry
import tkinter as tk
import datetime
from tkinter import Frame
from tkinter import Button, filedialog,Label,messagebox

#Declaracion de variables
Data_Libros = "Biblioteca/Libros.txt"
Data_Prestamos = "Biblioteca/Prestamos.txt"
Data_Devoluciones = "Biblioteca/Devoluciones.txt"
Data_User = "Biblioteca/Usuarios.txt"
Data_Prestamos_Morosida = "Biblioteca/Registro_Prestamos.txt"

class Prestamos:

    #Metodo constructor que crea la instancia con la ventana principal
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.libros_dic = {}
        self.usuarios_dic = {}

    #Con este metodo cargamos el archivo txt que contiene los libros guardados y obtenemos su isbn para 
    #cargarlos en los combobox
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

    #Con este metodo cargamos el archivo txt que contiene los usuraios guardados y obtenemos su id para 
    #cargarlos en los combobox 
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
                        messagebox.showerror(title="Error",message=f"Línea malformada detectada y omitida: {linea}")
        except FileNotFoundError:
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_User} no está creado aún")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error al cargar el archivo: {e}")
        return self.usuarios_dic

    # Llenar los ComboBox de préstamos con los datos de los archivos cargados
    def configurar_combo_boxes(self, combobox_id_usuario, combobox_isbn):
        
        usuarios = self.cargar_usuarios()
        libros = self.cargar_libros()
        combobox_id_usuario['values'] = list(usuarios.keys())
        combobox_isbn['values'] = list(libros.keys())   

    #Con este metodo se obtiene los datos seleccionados por el usuario en los combobox 
    #y se crea el archivo Prestamos.txt que guarda todos los datos de los prestamos realizados.
    def registrar_prestamo(self):
        usuario_id = self.combobox_id_usuario.get()
        libro_isbn = self.combobox_isbn.get()
        fecha_inicio = fecha_inicio_entry.get_date()
        
        if usuario_id and libro_isbn and fecha_inicio:
            try:
                with open(Data_Prestamos, 'a') as f:
                    f.write(f"Codigo ISBN: {libro_isbn}, ID Usuario: {usuario_id}, Fecha de Prestamo: {fecha_inicio}\n")

                #En esta parte se crea el archivo que lleva el registro de todos los prestamos realizados y 
                # que no se borra ya que se utiliza para calcular la morosidad de los prestamos
                with open(Data_Prestamos_Morosida, 'a') as f:
                    f.write(f"Codigo ISBN: {libro_isbn}, ID Usuario: {usuario_id}, Fecha de Prestamo: {fecha_inicio}\n")
                print(f"Préstamo registrado: {libro_isbn}, {usuario_id}, {fecha_inicio}")
                #En esta parte se actualizan los combobox cada vez que se agre un prestamo
                self.actualizar_combobox(libro_isbn)
                self.configurar_combo_boxes_devolver(self.combobox_id_devolver,self.combobox_isbn_devolver)
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error al registrar el préstamo: {e}")
        else:
            messagebox.showwarning(title="Advertencia",message="Por favor, complete todos los campos.")

    # Llenar los ComboBox de devoluciones con los datos de los préstamos actuales
    def configurar_combo_boxes_devolver(self, combobox_id_devolver, combobox_isbn_devolver):
        usuarios_prestamos, libros_prestamos = self.cargar_prestamos()
        combobox_id_devolver['values'] = usuarios_prestamos
        combobox_isbn_devolver['values'] = libros_prestamos

    #En este metodo se crea el archivo Devoluciones.txt que guarda los datos de las devoluciones realizadas.
    def devolver_libro(self):
        usuario_id = self.combobox_id_devolver.get().strip()
        libro_isbn = self.combobox_isbn_devolver.get().strip()
        fecha_entrega = fecha_entrega_entry.get_date()
        
        if usuario_id and libro_isbn and fecha_entrega:
            try:
                # Leer los datos de los préstamos existentes
                prestamos = []
                with open(Data_Prestamos, 'r') as f:
                    prestamos = f.readlines()
                
                # Formato de búsqueda basado en cómo se escribe en el archivo
                prestamo_buscar = f"Codigo ISBN: {libro_isbn}, ID Usuario: {usuario_id},"
                prestamo_encontrado = None
                
                # Lista para almacenar los préstamos actualizados
                prestamos_actualizados = []
                #Recorre el archivo de los prestamos para validar que los datos seleccionados en los combobox de devolucion 
                # existan y al encontrar una coincidencia lo guarda en el archivo txt de devoluciones
                for prestamo in prestamos:
                    prestamo_limpio = prestamo.strip()
                    #print(f"Buscando: '{prestamo_buscar}' en '{prestamo_limpio}'")
                    if prestamo_limpio.startswith(prestamo_buscar):
                        print(f"Préstamo encontrado: {prestamo_limpio}")
                        prestamo_encontrado = prestamo_limpio
                        # Guardar la devolución en el archivo de devoluciones
                        with open(Data_Devoluciones, 'a') as f:
                            f.write(f"Codigo ISBN: {libro_isbn}, ID Usuario: {usuario_id}, Fecha de Devolucion: {fecha_entrega}\n")
                    else:
                        prestamos_actualizados.append(prestamo)

                # Remover el préstamo del archivo de préstamos al agregar la devolucion al archivo
                if prestamo_encontrado:
                    
                    with open(Data_Prestamos, "w") as f:
                        f.writelines(prestamos_actualizados)
                    print(f"Devolución registrada: {libro_isbn}, {usuario_id}, {fecha_entrega}")
                    self.configurar_combo_boxes_devolver(self.combobox_id_devolver, self.combobox_isbn_devolver)
                else:
                    messagebox.showerror(title="Error",message="Préstamo no encontrado para devolución.")
            except Exception as e:
                messagebox.showerror(title="Error",message=f"Error al registrar la devolución: {e}")
        else:
            messagebox.showwarning(title="Advertencia",message="Por favor, complete todos los campos.")


    #En este metodo actualizamos los combobox cada vez que ocurre un cambio 
    def actualizar_combobox(self,isbn_libro = None,devolver=False):
        libros = self.cargar_libros()

        if devolver and isbn_libro:
            if isbn_libro not in libros:
                libros[isbn_libro] = {"titulo":"","autor":""}
        
        self.combobox_isbn["values"] = list(libros.keys())
        usuarios = self.cargar_usuarios()
        self.combobox_id_usuario["values"] = list(usuarios.keys())

        if devolver:
            self.configurar_combo_boxes_devolver(self.combobox_id_devolver,self.combobox_isbn_devolver)

    #Con este metodo se carga la informacion del archivo que contiene los prestamos realizados que 
    # sirve para llenar los combobox de las devoluciones y asi nunca se repitan los datos
    def cargar_prestamos(self):
        usuarios_prestamos = set()
        libros_prestamos = set()

        try:
            with open(Data_Prestamos, 'r') as archivo:
                for linea in archivo:
                    partes = linea.split(", ")
                    if len(partes) >= 3:
                        isbn = partes[0].split(": ")[1].strip()
                        usuario_id = partes[1].split(": ")[1].strip()
                        
                        usuarios_prestamos.add(usuario_id)
                        libros_prestamos.add(isbn)

        except FileNotFoundError:
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_Prestamos} no está creado aún")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error al cargar el archivo de préstamos: {e}")

        return list(usuarios_prestamos), list(libros_prestamos)

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

        self.combobox_isbn = ttk.Combobox(prestamos_Frame)
        self.combobox_isbn.pack()
        self.combobox_isbn.place(x=240, y=50, width=160, height=20)

        label_id_usuario = Label(prestamos_Frame, text="Seleccione el ID del Usuario", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=90, width=180, height=20)

        self.combobox_id_usuario = ttk.Combobox(prestamos_Frame)
        self.combobox_id_usuario.pack()
        self.combobox_id_usuario.place(x=240, y=90, width=160, height=20)

        self.configurar_combo_boxes(self.combobox_id_usuario,self.combobox_isbn)
        

        label_id_usuario = Label(prestamos_Frame, text="Seleccione la fecha del Prestamo", font=("Modern", 12), foreground="white")
        label_id_usuario.pack()
        label_id_usuario.config(bg="black")
        label_id_usuario.place(x=20, y=130, width=210, height=20)

        global fecha_inicio_entry
        fecha_inicio_entry = DateEntry(prestamos_Frame, date_pattern='yyyy-mm-dd')
        fecha_inicio_entry.pack()
        fecha_inicio_entry.place(x=240, y=130, width=160,height=20)

        label_isbn_devolver = Label(prestamos_Frame, text="Seleccione el ISBN del libro", font=("Modern", 12), foreground="white")
        label_isbn_devolver.pack()
        label_isbn_devolver.config(bg="black")
        label_isbn_devolver.place(x=20, y=160, width=190, height=20)

        self.combobox_isbn_devolver = ttk.Combobox(prestamos_Frame)
        self.combobox_isbn_devolver.pack()
        self.combobox_isbn_devolver.place(x=240, y=160, width=160, height=20)

        label_id_devolver = Label(prestamos_Frame, text="Seleccione el ID del Usuario", font=("Modern", 12), foreground="white")
        label_id_devolver.pack()
        label_id_devolver.config(bg="black")
        label_id_devolver.place(x=20, y=190, width=190, height=20)

        self.combobox_id_devolver = ttk.Combobox(prestamos_Frame)
        self.combobox_id_devolver.pack()
        self.combobox_id_devolver.place(x=240, y=190, width=160, height=20)
        self.configurar_combo_boxes_devolver(self.combobox_id_devolver, self.combobox_isbn_devolver)

        label_fecha_entrega = Label(prestamos_Frame, text="Seleccione la fecha de Entrega", font=("Modern", 12), foreground="white")
        label_fecha_entrega.pack()
        label_fecha_entrega.config(bg="black")
        label_fecha_entrega.place(x=20, y=220, width=190, height=20)

        global fecha_entrega_entry
        fecha_entrega_entry = DateEntry(prestamos_Frame, date_pattern='yyyy-mm-dd')
        fecha_entrega_entry.pack()
        fecha_entrega_entry.place(x=240, y=220, width=160,height=20)

        button_prestar = Button(prestamos_Frame, text="Prestar Libro", command= self.registrar_prestamo, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_prestar.pack()
        button_prestar.config(bg="black")
        button_prestar.place(x=430, y=130, width=110, height=20)

        button_devolver = Button(prestamos_Frame, text="Devolver Libro", command= self.devolver_libro, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_devolver.pack()
        button_devolver.config(bg="black")
        button_devolver.place(x=430, y=220, width=110, height=20)

        button_regresar = Button(prestamos_Frame, text="Regresar", command= lambda: self.regresar(self.ventana_prestamos), font=("Modern", 12), foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=430, y=265, width=110, height=20)

    
    #Este metodo sirve para ocultar la ventana en la que se trabaja al regresar a la ventana principal

    def regresar(self, ventana):
        ventana.destroy()
        self.ventana_principal.deiconify()
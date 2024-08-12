from tkinter import Tk,ttk,END
import tkinter as tk
from tkinter import Frame
from tkinter import Button, filedialog,Label,messagebox

#Variables globales
Data_File = "Usuarios.txt"
usuarios_dic = {}

class Usuarios:

    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.usuarios_dic = {}

    def cargar_usuarios(self):
        try:
            with open(Data_File, 'r') as archivo:
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
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_File} no está creado aún")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Ocurrió un error al cargar el archivo: {e}")



    #Con este metodo actualizo los valores que se agregan al combobox cada vez que se elimina un usuario
    def actualizar_combobox(self, combobox):
        combobox['values'] = list(self.usuarios_dic.keys())
        #combobox.current(0)
        print(list(self.usuarios_dic.keys()))

    #En este metodo leemos los valores ingresados por el usuario en los Entry y los guardamos en un archivo txt.
    def registar_usuarios(self):
        id_usuario = entrada_id.get()
        
        #Aqui se valida que el id del usuario aun no exista en los usuarios ya ingresados anteriormente.
        if id_usuario in self.usuarios_dic:
            messagebox.showerror(title="Error de Usuario", message=f"El ID de Usuario {id_usuario} ya existe en la biblioteca.")
            return
        nombre_usuario = entrada_nombre.get()
        #Aca se agregan los datos de los usuarios
        self.usuarios_dic[id_usuario] = {'Nombre Usuario': nombre_usuario, 'ID Usuario': id_usuario}
        
        # Guarda Los usuarios en un archivo de texto
        with open(Data_File, 'a') as archivo:
            archivo.write(f"Nombre del Usuario: {nombre_usuario}, ID del Usuario: {id_usuario}\n")
        
        messagebox.showinfo(title="Guardar Usuario", message=f"Usuario '{nombre_usuario}' agregado exitosamente.")
        print(self.usuarios_dic)
        
        # Limpia los cuadros de texto después de guardar un Usuario
        entrada_nombre.delete(0, END)
        entrada_id.delete(0, END)
        
        # Actualiza el ComboBox después de agregar un Usuario
        self.actualizar_combobox(combobox_eliminar)

    #Con este metodo seleccionamos el id  del usuario que se desea eliminar y se elimina del archivo 
    # de texto que contiene los usuarios guardados
    def eliminar_usuario(self):
        eliminar_id = combobox_eliminar.get()

        if not eliminar_id:
            messagebox.showwarning("Advertencia", "Seleccione un ID para eliminar.")
            return

        if eliminar_id not in self.usuarios_dic:
            messagebox.showwarning("Advertencia", "El ID seleccionado no existe.")
            return

        # Eliminar del diccionario el libro con el codigo elegido
        del self.usuarios_dic[eliminar_id]

        # Reescribir el archivo sin el libro eliminado
        with open(Data_File, 'w') as archivo:
            for id_key, info in self.usuarios_dic.items():
                archivo.write(f"Nombre del Usuario: {info["Nombre Usuario"]}, ID Usuario: {id_key}\n")

        messagebox.showinfo("Eliminar Usuario", f"El Usuario con ID '{eliminar_id}' eliminado exitosamente.")
        print(self.usuarios_dic)

        # Actualiza los ComboBox después de eliminar un usuario
        self.actualizar_combobox(combobox_eliminar)

    # Estructura y componentes de la ventana de Usuarios
    def ventana_Usuarios(self):
        self.cargar_usuarios()
        self.ventana_principal.iconify()
        self.ventana_usuarios = tk.Toplevel()
        self.ventana_usuarios.title("Gestionando Usuarios")
        self.ventana_usuarios.geometry("%dx%d+%d+%d" % (500, 300, 450, 220))
        self.ventana_usuarios.resizable(0, 0)

        usuarios_Frame = Frame(self.ventana_usuarios)
        usuarios_Frame.pack(side="top")
        usuarios_Frame.place(width="500", height="300")
        usuarios_Frame.config(bg="black")

        label_nombre = Label(usuarios_Frame, text="Nombre del Usuario", font=("Modern", 12), foreground="white")
        label_nombre.pack()
        label_nombre.config(bg="black")
        label_nombre.place(x=20, y=40, width=200, height=20)

        global entrada_nombre
        entrada_nombre = tk.Entry(usuarios_Frame)
        entrada_nombre.pack()
        entrada_nombre.place(x = 200, y = 40, width = 160, height = 20)

        label_id = Label(usuarios_Frame, text="ID Usuario", font=("Modern", 12), foreground="white")
        label_id.pack()
        label_id.config(bg="black")
        label_id.place(x=20, y=70, width=200, height=20)

        global entrada_id
        entrada_id = tk.Entry(usuarios_Frame)
        entrada_id.pack()
        entrada_id.place(x= 200, y=70, width=160, height=20)

        button_registrar_usuario = Button(usuarios_Frame, text="Registrar Usuario",command=self.registar_usuarios, font=("Modern", 12), foreground="white",highlightthickness=2)
        button_registrar_usuario.pack()
        button_registrar_usuario.config(bg="black")
        button_registrar_usuario.place(x=230, y=100, width=110, height=20)

        label_eliminar_usuario = Label(usuarios_Frame, text="Seleccione ID del Usuario", font=("Modern", 12), foreground="white")
        label_eliminar_usuario.pack()
        label_eliminar_usuario.config(bg="black")
        label_eliminar_usuario.place(x=20, y=180, width=200, height=20)

        global combobox_eliminar
        combobox_eliminar = ttk.Combobox(usuarios_Frame)
        combobox_eliminar.pack()
        combobox_eliminar.place(x=200, y=180, width=160, height=20)
        self.actualizar_combobox(combobox_eliminar)

        button_eliminar_usuario = Button(usuarios_Frame, text="Eliminar Usuario",command= self.eliminar_usuario, font=("Modern", 12), foreground="white",highlightthickness=2)
        button_eliminar_usuario.pack()
        button_eliminar_usuario.config(bg="black")
        button_eliminar_usuario.place(x=370, y=180, width=110, height=20)

        button_regresar = Button(usuarios_Frame, text="Regresar", command= lambda: self.regresar(self.ventana_usuarios), font=("Modern", 12), foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=370, y=255, width=110, height=20)
        
        self.ventana_usuarios.mainloop()

    #Este metodo sirve para ocultar la ventana en la que se trabaja al regresar a la ventana principal

    def regresar(self, ventana):
        ventana.destroy()
        self.ventana_principal.deiconify()
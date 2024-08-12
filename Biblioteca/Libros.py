#Importando las librerias
from tkinter import END, Tk, ttk
import tkinter as tk
from tkinter import Frame
from tkinter import Button, Label, Entry, messagebox

#Variables globales
Data_File = "Libros.txt"
libros_dic = {}

class Libros:
    #Metodo constructor que contiene la instancia de la ventana principal 
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.libros_dic = {}
    
    #En este metodo se carga el archivo creado con los libros y se recorre 
    # para obtener el isbn de los libros agregados al diccionario, 
    # este metodo ayuda a obtener el codigo que sirve para eliminar los libros
    def cargar_libros(self):
        try:
            with open(Data_File, 'r') as archivo:
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
            messagebox.showwarning(title="Carga de Archivo", message=f"Advertencia, El archivo {Data_File} no esta creado aun")
    

    #Con este metodo actualizo los valores que se agregan al combobox cada vez que se guarda o elimina un libro
    def actualizar_combobox(self, combobox):
        combobox['values'] = list(self.libros_dic.keys())
        combobox.current(0)
        print(list(self.libros_dic.keys()))

    #En este metodo leemos los valores ingresados por el usuario el los Entry y los guardamos en un archivo txt.
    def guardar_libros(self):
        isbn = entrada_isbn.get()

        #Aqui se valida que el isbn del libro aun no exista en los libros ya ingresados anteriormente.
        if isbn in self.libros_dic:
            messagebox.showerror(title="Error de Codigo", message=f"El ISBN {isbn} ya existe en la biblioteca.")
            return
        titulo = entrada_nombre.get()
        autor = entrada_autor.get()
        #Aca se agregan los dats 
        self.libros_dic[isbn] = {'titulo': titulo, 'autor': autor}
        
        # Guarda Los libros en un archivo de texto
        with open(Data_File, 'a') as archivo:
            archivo.write(f"Nombre del Libro: {titulo}, Autor: {autor}, Codigo ISBN: {isbn}\n")
        
        messagebox.showinfo(title="Guardar Libro", message=f"Libro '{titulo}' agregado exitosamente.")
        print(self.libros_dic)
        
        # Limpia los cuadros de texto después de guardar un libro
        entrada_autor.delete(0, END)
        entrada_isbn.delete(0, END)
        entrada_nombre.delete(0, END)
        
        # Actualiza el ComboBox después de agregar un libro
        self.actualizar_combobox(combobox_eliminar)
        self.actualizar_combobox_buscar(combobox_buscar)

    #Con este metodo seleccionamos un codigo isbn del libro que se desea eliminar y se elimina del archivo de texto que contiene los libros guardados
    def eliminar_libro(self):
        eliminar_isbn = combobox_eliminar.get()

        if not eliminar_isbn:
            messagebox.showwarning("Advertencia", "Seleccione un ISBN para eliminar.")
            return

        if eliminar_isbn not in self.libros_dic:
            messagebox.showwarning("Advertencia", "El ISBN seleccionado no existe.")
            return

        # Eliminar del diccionario el libro con el codigo elegido
        del self.libros_dic[eliminar_isbn]

        # Reescribir el archivo sin el libro eliminado
        with open(Data_File, 'w') as archivo:
            for isbn_key, info in self.libros_dic.items():
                archivo.write(f"Nombre del Libro: {info['titulo']}, Autor: {info['autor']}, Codigo ISBN: {isbn_key}\n")

        messagebox.showinfo("Eliminar Libro", f"Libro con ISBN '{eliminar_isbn}' eliminado exitosamente.")
        #print(self.libros_dic)

        # Actualiza los ComboBox después de eliminar un libro
        self.actualizar_combobox(combobox_eliminar)

    #Este metodo se encarga de actualizar el combobox de busqueda con cada vez que se agregue un libro nuevo o elimine.
    def actualizar_combobox_buscar(self, combobox):
        # Agrega al  ComboBox los títulos de los libros que se cargan del archivo txt
        titulos = list(set(info['titulo'] for info in self.libros_dic.values()))
        combobox['values'] = titulos
        if titulos:
            combobox.current(0)  # Opcional: Selecciona el primer elemento si hay alguno

    #Con este metodo se realiza la busqueda del libro por medio del titulo seleccionado en el combobox.
    def buscar_libro(self):
        titulo_buscar = combobox_buscar.get()
        if not titulo_buscar:
            messagebox.showwarning("Advertencia", "Seleccione un título para buscar.")
            return
        resultados = [f"El libro buscado es : \n Titulo: {titulo_buscar}, ISBN: {isbn}, Autor: {info['autor']}" 
                      for isbn, info in self.libros_dic.items() 
                      if info['titulo'] == titulo_buscar]

        if not resultados:
            messagebox.showinfo("Buscar Libro", "No se encontraron libros con ese título.")
        else:
            messagebox.showinfo("Buscar Libro", "\n".join(resultados))
        self.actualizar_combobox_buscar(combobox_buscar)
        


    #Este metodo contiene todos los elementos para crear la ventana en la que se gestionan los libros
    def ventana_Libros(self):
        self.cargar_libros()
        self.ventana_principal.iconify()
        self.ventana_libros = tk.Toplevel()
        self.ventana_libros.title("Gestionando Libros")
        self.ventana_libros.geometry("%dx%d+%d+%d" % (500, 300, 450, 220))
        self.ventana_libros.resizable(0, 0)

        libros_Frame = Frame(self.ventana_libros)
        libros_Frame.pack(side="top")
        libros_Frame.place(width="500", height="300")
        libros_Frame.config(bg="black")

        label_nombre = Label(libros_Frame, text="Titulo del Libro", font=("Modern", 12), foreground="white")
        label_nombre.pack()
        label_nombre.config(bg="black")
        label_nombre.place(x=20, y=40, width=200, height=20)
        
        global entrada_nombre
        entrada_nombre = tk.Entry(libros_Frame)
        entrada_nombre.pack()
        entrada_nombre.place(x=200, y=40, width=160, height=20)

        label_autor = Label(libros_Frame, text="Nombre del Autor", font=("Modern", 12), foreground="white")
        label_autor.pack()
        label_autor.config(bg="black")
        label_autor.place(x=20, y=70, width=200, height=20)

        global entrada_autor
        entrada_autor = tk.Entry(libros_Frame)
        entrada_autor.pack()
        entrada_autor.place(x=200, y=70, width=160, height=20)

        label_isbn = Label(libros_Frame, text="Ingrese el ISBN del libro", font=("Modern", 12), foreground="white")
        label_isbn.pack()
        label_isbn.config(bg="black")
        label_isbn.place(x=20, y=100, width=200, height=20)

        global entrada_isbn
        entrada_isbn = tk.Entry(libros_Frame)
        entrada_isbn.pack()
        entrada_isbn.place(x=200, y=100, width=160, height=20)

        button_guardar = Button(libros_Frame, text="Guardar Libro", command=self.guardar_libros, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_guardar.pack()
        button_guardar.config(bg="black")
        button_guardar.place(x=370, y=100, width=110, height=20)

        label_eliminar = Label(libros_Frame, text="Seleccione el ISBN", font=("Modern", 12), foreground="white")
        label_eliminar.pack()
        label_eliminar.config(bg="black")
        label_eliminar.place(x=20, y=180, width=200, height=20)

        global combobox_eliminar
        combobox_eliminar = ttk.Combobox(libros_Frame)
        combobox_eliminar.pack()
        combobox_eliminar.place(x=200, y=180, width=160, height=20)
        self.actualizar_combobox(combobox_eliminar)

        button_eliminar = Button(libros_Frame, text="Eliminar Libro",command= self.eliminar_libro, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_eliminar.pack()
        button_eliminar.config(bg="black")
        button_eliminar.place(x=370, y=180, width=110, height=20)

        label_buscar = Label(libros_Frame, text="Seleccione el Título", font=("Modern", 12), foreground="white")
        label_buscar.pack()
        label_buscar.config(bg="black")
        label_buscar.place(x=20, y=220, width=200, height=20)

        global combobox_buscar
        combobox_buscar = ttk.Combobox(libros_Frame)
        combobox_buscar.pack()
        combobox_buscar.place(x=200, y=220, width=160, height=20)
        self.actualizar_combobox_buscar(combobox_buscar)

        button_buscar = Button(libros_Frame, text="Buscar Libro", command= self.buscar_libro, font=("Modern", 12), foreground="white", highlightthickness=2)
        button_buscar.pack()
        button_buscar.config(bg="black")
        button_buscar.place(x=370, y=220, width=110, height=20)

        button_regresar = Button(libros_Frame, text="Regresar", command=lambda: self.regresar(self.ventana_libros), font=("Modern", 12), foreground="white", highlightthickness=2)
        button_regresar.pack()
        button_regresar.config(bg="black")
        button_regresar.place(x=370, y=265, width=110, height=20)

        self.ventana_libros.mainloop()

    
     #Este metodo sirve para ocultar la ventana en la que se trabaja al regresar a la ventana principal

    def regresar(self, ventana):
        ventana.destroy()
        self.ventana_principal.deiconify()



    




    


    

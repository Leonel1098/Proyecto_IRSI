import os
from tkinter import filedialog


class Utilidades:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal

    # ESte metodo sirve para abrir el cuadro de diálogo de selección de archivo y abrir los 
    # archivos de texto creados por el programa
    def abrir_archivo(self):
    
        archivo_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
        )
        if archivo_path:
            try:
                os.startfile(archivo_path) 
            except Exception as e:
                print(f"No se pudo abrir el archivo: {e}")
        else:
            print("No se seleccionó ningún archivo.")
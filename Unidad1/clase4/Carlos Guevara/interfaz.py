import tkinter as tk
import tkinter.messagebox as mesagebox
from libro import Libro

class Interfaz:
    def __init__(self):
        self.ventanaPrincipal = tk.Tk()

    def accion_guardar_boton(self, titulo):
        mesagebox.showinfo("Guardar", f"Guardando: titulo: {titulo}")

    def mostrar_interfaz(self):
        libro = Libro(self.ventanaPrincipal)

        labelTitulo = tk.Label(self.ventanaPrincipal, text="Título")
        entryTitulo = tk.Entry(self.ventanaPrincipal, textvariable=libro.titulo)

        boton_guardar = tk.Button(self.ventanaPrincipal,
                                   text="Guardar",
                                     command=lambda: self.accion_guardar_boton(libro.titulo.get()))

        self.ventanaPrincipal.title("Ventana Principal")
        self.ventanaPrincipal.geometry("300x300")
        labelTitulo.pack()
        entryTitulo.pack()
        boton_guardar.pack()
        
        self.ventanaPrincipal.mainloop()

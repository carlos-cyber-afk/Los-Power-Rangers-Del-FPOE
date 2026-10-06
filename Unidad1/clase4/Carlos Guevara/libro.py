import tkinter as tk
 
class Libro:
    def __init__(self, ventanaPrincipal):
        self.ventanaPrincipal = ventanaPrincipal
        self.titulo = tk.StringVar(ventanaPrincipal)
        self.paginas = tk.StringVar(ventanaPrincipal, value="1")
        self.fecha_publicacion = tk.StringVar(ventanaPrincipal, value="")
        self.disponible = tk.BooleanVar(ventanaPrincipal)
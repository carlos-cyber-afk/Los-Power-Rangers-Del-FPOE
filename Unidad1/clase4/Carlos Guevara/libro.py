import tkinter as tk

class Libro:
    def __init__(self, ventanaPrincipal):
        self.ventanaPrincipal = ventanaPrincipal
        self.titulo = tk.StringVar(ventanaPrincipal)

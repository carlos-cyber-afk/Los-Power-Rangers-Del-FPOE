import tkinter as tk

class Uva():

    def __init__(self, ventana_principal):

        self.ventana_principal = ventana_principal
        self.textura = tk.StringVar(ventana_principal)
        self.forma = tk.StringVar(ventana_principal)
        self.tamaño = tk.IntVar(ventana_principal)
        self.peso = tk.DoubleVar(ventana_principal)

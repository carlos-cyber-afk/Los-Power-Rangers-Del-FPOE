import tkinter as tk

class Uva():

    def __init__(self, ventana_principal):

        self.ventana_principal = ventana_principal
        self.textura = tk.StringVar(ventana_principal, value="")
        self.forma = tk.StringVar(ventana_principal, value="")
        self.tamaño = tk.IntVar(ventana_principal, value=5)
        self.peso = tk.StringVar(ventana_principal, value=0.0)
import tkinter as tk


class Asignatura():

    def __init__(self, ventana_principal):
        self.textura = tk.StringVar(ventana_principal)
        self.forma = tk.StringVar(ventana_principal)
        self.tamaño = tk.IntVar(ventana_principal)
        self.peso = tk.FloatVar(ventana_principal)

    def limpiar(self):
        self.textura.set('')
        self.forma.set('')
        self.tamaño.set(0)
        self.peso.set(0.0)

    def a_diccionario(self):
        return {
            'textura': self.textura.get().strip(),
            'formaa': self.forma.get().strip(),
            'tamaño': self.tamaño.get(),
            'peso': self.peso.get(),
        }
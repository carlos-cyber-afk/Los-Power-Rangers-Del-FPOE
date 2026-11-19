import tkinter as tk


class Uva():

    def __init__(self, ventana_principal):
        self.id = None
        self.textura = tk.StringVar(ventana_principal)
        self.forma = tk.StringVar(ventana_principal)
        self.tamaño = tk.StringVar(ventana_principal)
        self.peso = tk.StringVar(ventana_principal)

    def cargar(self, datos):
        self.id = datos['id']
        self.textura.set(datos['textura'])
        self.forma.set(datos['forma'])
        self.tamaño.set(datos['tamano'])
        self.peso.set(datos['peso'])

    def limpiar(self):
        self.id = None
        self.textura.set('')
        self.forma.set('')
        self.tamaño.set('')
        self.peso.set('')

    def a_diccionario(self):
        return {
            'textura': self.textura.get().strip(),
            'forma': self.forma.get().strip(),
            'tamano': int(self.tamaño.get().strip()),
            'peso': float(self.peso.get().strip().replace(',', '.')),
        }
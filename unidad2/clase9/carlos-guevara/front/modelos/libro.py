import tkinter as tk


class Libro():

    def __init__(self, ventana_principal):
        self.titulo = tk.StringVar(ventana_principal)
        self.paginas = tk.StringVar(ventana_principal)
        self.fecha_publicacion = tk.StringVar(ventana_principal)
        self.disponible = tk.BooleanVar(ventana_principal, value=True)

    def limpiar(self):
        self.titulo.set('')
        self.paginas.set('')
        self.fecha_publicacion.set('')
        self.disponible.set(True)

    def a_diccionario(self):
        return {
            'titulo': self.titulo.get().strip(),
            'paginas': int(self.paginas.get()),
            'fecha_publicacion': self.fecha_publicacion.get().strip(),
            'disponible': self.disponible.get(),
        }
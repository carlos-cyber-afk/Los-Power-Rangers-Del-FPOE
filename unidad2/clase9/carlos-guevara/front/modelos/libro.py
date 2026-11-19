import tkinter as tk
from datetime import datetime


class Libro():

    def __init__(self, ventana_principal):
        self.id = None
        self.titulo = tk.StringVar(ventana_principal)
        self.paginas = tk.StringVar(ventana_principal)
        self.fecha_publicacion = tk.StringVar(ventana_principal)
        self.disponible = tk.BooleanVar(ventana_principal, value=True)

    def limpiar(self):
        self.id = None
        self.titulo.set('')
        self.paginas.set('')
        self.fecha_publicacion.set('')
        self.disponible.set(True)

    def cargar(self, registro):
        self.id = registro['id']
        self.titulo.set(registro['titulo'])
        self.paginas.set(str(registro['paginas']))
        self.fecha_publicacion.set(self.fecha_a_pantalla(registro['fecha_publicacion']))
        self.disponible.set(registro['disponible'])

    def a_diccionario(self):
        return {
            'titulo': self.titulo.get().strip(),
            'paginas': int(self.paginas.get()),
            'fecha_publicacion': self.fecha_a_api(self.fecha_publicacion.get()),
            'disponible': self.disponible.get(),
        }

    @staticmethod
    def fecha_a_pantalla(texto):
        return datetime.strptime(texto, '%Y-%m-%d').strftime('%d/%m/%Y')

    @staticmethod
    def fecha_a_api(texto):
        return datetime.strptime(texto.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
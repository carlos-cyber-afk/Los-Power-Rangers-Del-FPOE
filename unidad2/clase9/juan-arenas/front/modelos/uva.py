import tkinter as tk


class Uva():

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
    def __init__(self, ventana_principal):
        self.id = None
        self.nombre = tk.StringVar(ventana_principal)
        self.creditos = tk.StringVar(ventana_principal)
        self.clases_por_programar = tk.StringVar(ventana_principal)
        self.activa = tk.BooleanVar(ventana_principal, value=True)
        self.fecha_inicio = tk.StringVar(ventana_principal)

    def cargar(self, datos):
       self.id = datos['id']
       self.nombre.set(datos['nombre'])
       self.creditos.set(datos['creditos'])
       self.clases_por_programar.set(datos['clases_por_programar'])
       self.activa.set(datos['activa'])
       self.fecha_inicio.set(datos['fecha_inicio'])
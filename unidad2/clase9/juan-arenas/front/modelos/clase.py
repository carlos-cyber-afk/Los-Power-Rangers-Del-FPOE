import tkinter as tk


class Clase():

    MODALIDADES = ('PRESENCIAL', 'VIRTUAL')

    def __init__(self, ventana_principal):
        self.id = None
        self.uva = tk.StringVar(ventana_principal)
        self.forma = tk.StringVar(ventana_principal)
        self.textura = tk.StringVar(ventana_principal)
        self.tamaño = tk.IntVar(ventana_principal)
        self.peso = tk.FloatVar(ventana_principal)
        self.modalidad = tk.StringVar(ventana_principal, value='PRESENCIAL')

    def cargar(self, datos):
        self.id = datos['id']
        self.asignatura.set(datos['uva_id'])
        self.forma.set(datos['formar'])
        self.textura.set(datos['textura'])
        self.tamaño.set(datos['tamaño'])
        self.peso.set(datos['peso'])
        self.modalidad.set(datos['modalidad'])

    def limpiar(self):
        self.id = None
        self.asignatura.set('')
        self.forma.set('')
        self.textura.set('')
        self.tamaño.set(0)
        self.peso.set(0.0)
        self.modalidad.set('PRESENCIAL')

    def a_diccionario(self, id_uva):
        return {
            'uva': id_uva,
            'forma': self.forma.get().strip(),
            'textura': self.textura.get().strip(),
            'tamaño': self.tamaño.get().strip(),
            'peso': self.peso.get().strip(),
            'modalidad': self.modalidad.get(),
        }

    
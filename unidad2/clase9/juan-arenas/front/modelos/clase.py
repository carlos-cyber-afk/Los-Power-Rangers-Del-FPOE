import tkinter as tk


class Clase():

    MODALIDADES = ('PRESENCIAL', 'VIRTUAL')

    def __init__(self, ventana_principal):
        self.id = None
        self.uva = tk.StringVar(ventana_principal)
        self.forma = tk.StringVar(ventana_principal)
        self.textura = tk.StringVar(ventana_principal)
        self.tamaño = tk.StringVar(ventana_principal)
        self.peso = tk.StringVar(ventana_principal)
        self.modalidad = tk.StringVar(ventana_principal, value='PRESENCIAL')

    def cargar(self, datos, etiqueta_uva=''):
        self.id = datos['id']
        self.uva.set(etiqueta_uva)
        self.forma.set(datos['forma'])
        self.textura.set(datos['textura'])
        self.tamaño.set(datos['tamano'])
        self.peso.set(datos['peso'])
        self.modalidad.set(datos['modalidad'])

    def limpiar(self):
        self.id = None
        self.uva.set('')
        self.forma.set('')
        self.textura.set('')
        self.tamaño.set('')
        self.peso.set('')
        self.modalidad.set('PRESENCIAL')

    def a_diccionario(self, id_uva):
        return {
            'uva': id_uva,
            'forma': self.forma.get().strip(),
            'textura': self.textura.get().strip(),
            'tamano': int(self.tamaño.get().strip()),
            'peso': float(self.peso.get().strip().replace(',', '.')),
            'modalidad': self.modalidad.get(),
        }
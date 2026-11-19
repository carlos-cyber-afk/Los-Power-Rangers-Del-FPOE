from tkinter import ttk

from controladores.validaciones import Validaciones
from modelos.uva import Uva
from vistas.vista_base import VistaBase


class VistaUva(VistaBase):

    titulo_formulario = 'Datos de la uva'
    recurso = 'uvas'
    columnas = (
        ('id', 'Id', 50),
        ('textura', 'Textura', 220),
        ('forma', 'Forma', 220),
        ('tamano', 'Tamaño (1-10)', 110),
        ('peso', 'Peso', 90),
    )

    def crear_modelo(self):
        return Uva(self)

    def crear_campos(self, marco):
        entry_textura = ttk.Entry(marco, textvariable=self.modelo.textura)
        entry_forma = ttk.Entry(marco, textvariable=self.modelo.forma)
        spin_tamaño = ttk.Spinbox(marco, from_=1, to=10, textvariable=self.modelo.tamaño)
        entry_peso = ttk.Entry(marco, textvariable=self.modelo.peso)

        self.agregar_campo(marco, 0, 0, 'Textura', entry_textura)
        self.agregar_campo(marco, 0, 2, 'Forma', entry_forma)
        self.agregar_campo(marco, 1, 0, 'Tamaño (1 a 10)', spin_tamaño)
        self.agregar_campo(marco, 1, 2, 'Peso (0.1 a 15)', entry_peso)

    def validar(self):
        return Validaciones.validarUva(self.modelo)

    def datos_formulario(self):
        return self.modelo.a_diccionario()

    def valores_fila(self, registro):
        return (
            registro['id'],
            registro['textura'],
            registro['forma'],
            registro['tamano'],
            registro['peso'],
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Eliminar la uva #' + str(registro['id']) + ' (' + registro['forma'] + ', ' + registro['textura'] + ')?'
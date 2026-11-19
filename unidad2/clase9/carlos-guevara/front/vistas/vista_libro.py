from tkinter import ttk

from tkcalendar import DateEntry

from vistas.vista_base import VistaBase
from modelos.libro import Libro
from controladores.validaciones import Validaciones

ROJO = '#b00020'


class VistaLibro(VistaBase):

    titulo_formulario = 'Libro'
    recurso = 'libros'
    columnas = (
        ('titulo', 'Título', 250),
        ('paginas', 'Páginas', 80),
        ('fecha_publicacion', 'Fecha de publicación', 140),
        ('disponible', 'Disponible', 90),
    )

    def crear_modelo(self):
        return Libro(self)

    def crear_campos(self, marco):
        modelo = self.modelo
        self.etiquetas_error = {}

        entrada_titulo = ttk.Entry(marco, textvariable=modelo.titulo)
        self.agregar_campo(marco, 0, 0, 'Título:', entrada_titulo)
        self.agregar_error(marco, 1, 1, 'titulo', entrada_titulo,
                           modelo.titulo, Validaciones.validarTitulo)

        entrada_paginas = ttk.Spinbox(marco, from_=1, to=5000, textvariable=modelo.paginas)
        self.agregar_campo(marco, 0, 2, 'Páginas:', entrada_paginas)
        revisar_paginas = self.agregar_error(marco, 1, 3, 'paginas', entrada_paginas,
                                             modelo.paginas, Validaciones.validarPaginas)
        entrada_paginas.config(command=revisar_paginas)  # valida también con las flechas

        entrada_fecha = DateEntry(marco, textvariable=modelo.fecha_publicacion,
                                  date_pattern='dd/mm/yyyy', locale='es_ES')
        self.agregar_campo(marco, 2, 0, 'Fecha de publicación:', entrada_fecha)
        self.agregar_error(marco, 3, 1, 'fecha_publicacion', entrada_fecha,
                           modelo.fecha_publicacion, Validaciones.validarFechaPublicacion,
                           eventos=('<KeyRelease>', '<<DateEntrySelected>>'))

        casilla = ttk.Checkbutton(marco, text='Disponible', variable=modelo.disponible)
        casilla.grid(row=2, column=2, columnspan=2, sticky='w', pady=4)

    def agregar_error(self, marco, fila, columna, clave, campo, variable, validador,
                      eventos=('<KeyRelease>',)):
        etiqueta = ttk.Label(marco, foreground=ROJO)
        etiqueta.grid(row=fila, column=columna, sticky='w', pady=(0, 4))
        self.etiquetas_error[clave] = etiqueta

        def revisar(evento=None):
            etiqueta.config(text=validador(variable.get()) or '')

        for evento in eventos:
            campo.bind(evento, revisar)
        return revisar

    def limpiar_errores(self):
        for etiqueta in self.etiquetas_error.values():
            etiqueta.config(text='')

    def accion_limpiar(self):
        super().accion_limpiar()
        self.limpiar_errores()

    def al_seleccionar(self, evento):
        super().al_seleccionar(evento)
        self.limpiar_errores()

    def validar(self):
        return Validaciones.validarLibro(self.modelo)

    def datos_formulario(self):
        return self.modelo.a_diccionario()

    def valores_fila(self, registro):
        return (
            registro['titulo'],
            registro['paginas'],
            Libro.fecha_a_pantalla(registro['fecha_publicacion']),
            'Sí' if registro['disponible'] else 'No',
        )

    def texto_confirmar_eliminar(self, registro):
        return f"¿Eliminar el libro «{registro['titulo']}»?"
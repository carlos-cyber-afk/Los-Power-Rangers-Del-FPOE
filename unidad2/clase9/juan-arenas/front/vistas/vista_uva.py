from tkinter import messagebox, ttk

from controladores.comunicacion import ErrorComunicacion
from controladores.validaciones import Validaciones
from modelos.uva import Uva 
from vistas.vista_base import VistaBase


class VistaAsignaturas(VistaBase):

    titulo_formulario = 'Datos de la asignatura'
    recurso = 'asignaturas'
    columnas = (
        ('id', 'Id', 40),
        ('nombre', 'Nombre', 230),
        ('creditos', 'Créditos', 70),
        ('activa', 'Activa', 60),
        ('fecha_inicio', 'Fecha de inicio', 110),
        ('clases_por_programar', 'Por programar', 100),
        ('total_clases', 'Clases', 60),
        ('total_horas', 'Horas', 60),
    )

    def crear_modelo(self):
        return Uva(self)

    def crear_campos(self, marco):
        entry_nombre = ttk.Entry(marco, textvariable=self.modelo.nombre)
        entry_creditos = ttk.Entry(marco, textvariable=self.modelo.creditos)
        entry_fecha = ttk.Entry(marco, textvariable=self.modelo.fecha_inicio)
        entry_clases = ttk.Entry(marco, textvariable=self.modelo.clases_por_programar)
        check_activa = ttk.Checkbutton(marco, text='Activa', variable=self.modelo.activa)

        self.agregar_campo(marco, 0, 0, 'Nombre', entry_nombre)
        self.agregar_campo(marco, 0, 2, 'Créditos (1 a 10)', entry_creditos)
        self.agregar_campo(marco, 1, 0, 'Fecha de inicio (AAAA-MM-DD)', entry_fecha)
        self.agregar_campo(marco, 1, 2, 'Clases por programar', entry_clases)
        check_activa.grid(row=2, column=0, columnspan=2, sticky='w', pady=4)

    def crear_botones_extra(self, marco):
        self.boton_estado = ttk.Button(marco, text='Desactivar', command=self.accion_cambiar_estado)
        self.boton_estado.pack(side='left', padx=(24, 0))

    def actualizar_botones(self):
        super().actualizar_botones()
        registro = self.registros.get(self.modelo.id)
        if registro is None:
            self.boton_estado.state(['disabled'])
        else:
            self.boton_estado.state(['!disabled'])
            self.boton_estado.config(text='Desactivar' if registro['activa'] else 'Activar')

    def accion_cambiar_estado(self):
        registro = self.registros[self.modelo.id]
        cambio = {'activa': not registro['activa']}
        try:
            self.comunicacion.modificar(self.recurso, registro['id'], cambio)
        except ErrorComunicacion as error:
            messagebox.showerror('No se pudo cambiar el estado', str(error))
            return
        self.refrescar('Asignatura activada.' if cambio['activa'] else 'Asignatura desactivada.')

    def validar(self):
        return Validaciones.validarAsignatura(self.modelo)

    def datos_formulario(self):
        return self.modelo.a_diccionario()

    def valores_fila(self, registro):
        return (
            registro['id'],
            registro['nombre'],
            registro['creditos'],
            'Sí' if registro['activa'] else 'No',
            registro['fecha_inicio'],
            registro['clases_por_programar'],
            registro['total_clases'],
            format(registro['total_horas'], 'g'),
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Eliminar la asignatura ' + registro['nombre'] + '?'
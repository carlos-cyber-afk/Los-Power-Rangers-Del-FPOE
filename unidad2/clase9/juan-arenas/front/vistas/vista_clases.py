import tkinter as tk
from tkinter import ttk

from controladores.validaciones import Validaciones
from modelos.clase import Clase
from vistas.vista_base import VistaBase

TODAS = 'Todas'


class VistaClases(VistaBase):

    titulo_formulario = 'Datos de la clase'
    recurso = 'clases'
    columnas = (
        ('id', 'Id', 50),
        ('uva', 'Uva', 200),
        ('forma', 'Forma', 130),
        ('textura', 'Textura', 130),
        ('tamano', 'Tamaño', 70),
        ('peso', 'Peso', 70),
        ('modalidad', 'Modalidad', 110),
    )

    def crear_modelo(self):
        self.uvas = {}        # etiqueta -> id
        self.etiquetas = {}   # id -> etiqueta
        self.id_filtro = None
        return Clase(self)

    @staticmethod
    def etiqueta_uva(uva):
        # Las uvas no tienen nombre, se identifican por id, forma y textura
        return '#' + str(uva['id']) + ' ' + uva['forma'] + ' / ' + uva['textura']

    @staticmethod
    def id_uva_de(clase):
        # El back puede devolver la uva como "uva_id" o como "uva"
        return clase.get('uva_id', clase.get('uva'))

    def crear_campos(self, marco):
        self.combo_uva = ttk.Combobox(marco, textvariable=self.modelo.uva, state='readonly')
        combo_modalidad = ttk.Combobox(
            marco, textvariable=self.modelo.modalidad, values=Clase.MODALIDADES, state='readonly'
        )
        entry_forma = ttk.Entry(marco, textvariable=self.modelo.forma)
        entry_textura = ttk.Entry(marco, textvariable=self.modelo.textura)
        spin_tamaño = ttk.Spinbox(marco, from_=1, to=10, textvariable=self.modelo.tamaño)
        entry_peso = ttk.Entry(marco, textvariable=self.modelo.peso)

        self.agregar_campo(marco, 0, 0, 'Uva', self.combo_uva)
        self.agregar_campo(marco, 0, 2, 'Modalidad', combo_modalidad)
        self.agregar_campo(marco, 1, 0, 'Forma', entry_forma)
        self.agregar_campo(marco, 1, 2, 'Textura', entry_textura)
        self.agregar_campo(marco, 2, 0, 'Tamaño (1 a 10)', spin_tamaño)
        self.agregar_campo(marco, 2, 2, 'Peso (0.1 a 15)', entry_peso)

    def crear_botones_extra(self, marco):
        self.filtro = tk.StringVar(self, value=TODAS)
        etiqueta = ttk.Label(marco, text='Ver clases de')
        self.combo_filtro = ttk.Combobox(marco, textvariable=self.filtro, state='readonly', width=28)
        self.label_total = ttk.Label(marco)

        etiqueta.pack(side='left', padx=(24, 6))
        self.combo_filtro.pack(side='left')
        self.label_total.pack(side='left', padx=12)

        self.combo_filtro.bind('<<ComboboxSelected>>', self.al_cambiar_filtro)

    def consultar_registros(self):
        uvas = self.comunicacion.listar('uvas')
        clases = self.comunicacion.listar('clases')
        return {'uvas': uvas, 'clases': clases}

    def mostrar_registros(self, datos):
        uvas = datos['uvas']
        self.etiquetas = {uva['id']: self.etiqueta_uva(uva) for uva in uvas}
        self.uvas = {etiqueta: id for id, etiqueta in self.etiquetas.items()}
        etiquetas = list(self.uvas)
        self.combo_uva.config(values=etiquetas)
        self.combo_filtro.config(values=[TODAS] + etiquetas)

        # Si la uva del filtro ya no existe, se vuelve a mostrar todo
        if self.id_filtro is not None and self.id_filtro not in self.etiquetas:
            self.id_filtro = None
        self.filtro.set(TODAS if self.id_filtro is None else self.etiquetas[self.id_filtro])

        clases = datos['clases']
        if self.id_filtro is not None:
            clases = [c for c in clases if self.id_uva_de(c) == self.id_filtro]

        peso_total = sum(float(clase['peso']) for clase in clases)
        self.label_total.config(
            text=str(len(clases)) + ' clases, peso total ' + format(peso_total, 'g')
        )
        super().mostrar_registros(clases)

    def cargar_modelo(self, registro):
        etiqueta = self.etiquetas.get(self.id_uva_de(registro), '')
        self.modelo.cargar(registro, etiqueta)

    def validar(self):
        errores = Validaciones.validarClase(self.modelo)
        etiqueta = self.modelo.uva.get()
        if etiqueta and etiqueta not in self.uvas:
            errores.append('Uva: ya no existe. Consulte de nuevo.')
        return errores

    def datos_formulario(self):
        id_uva = self.uvas[self.modelo.uva.get()]
        return self.modelo.a_diccionario(id_uva)

    def valores_fila(self, registro):
        return (
            registro['id'],
            self.etiquetas.get(self.id_uva_de(registro), ''),
            registro['forma'],
            registro['textura'],
            registro['tamano'],
            registro['peso'],
            registro['modalidad'],
        )

    def texto_confirmar_eliminar(self, registro):
        return '¿Eliminar la clase #' + str(registro['id']) + '?'

    def al_cambiar_filtro(self, evento):
        self.id_filtro = self.uvas.get(self.filtro.get())
        self.refrescar()
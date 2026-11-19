def crear_modelo(self):
        self.uva = {}
        self.id_filtro = None
        return Clase(self)

def crear_campos(self, marco):
    self.combo_asignatura = ttk.Combobox(
        marco, textvariable=self.modelo.asignatura, state='readonly'
    )
    combo_modalidad = ttk.Combobox(
        marco, textvariable=self.modelo.modalidad, values=Clase.MODALIDADES, state='readonly'
    )
    entry_tema = ttk.Entry(marco, textvariable=self.modelo.tema)
    entry_fecha = ttk.Entry(marco, textvariable=self.modelo.fecha)
    entry_hora = ttk.Entry(marco, textvariable=self.modelo.hora_inicio)
    entry_duracion = ttk.Entry(marco, textvariable=self.modelo.duracion_horas)

    self.agregar_campo(marco, 0, 0, 'uva', self.combo_uva)
    self.agregar_campo(marco, 0, 2, 'forma', entry_forma)
    self.agregar_campo(marco, 1, 0, 'F (textura', entry_textura)
    self.agregar_campo(marco, 1, 2, 'Hora de inicio (HH:MM)', entry_hora)
    self.agregar_campo(marco, 2, 0, 'Duración en horas (0.5 a 4)', entry_duracion)
    self.agregar_campo(marco, 2, 2, 'Modalidad', combo_modalidad)

def consultar_registros(self):
    asignaturas = self.comunicacion.listar('asignaturas')
    filtros = {'asignatura': self.id_filtro} if self.id_filtro else None
    clases = self.comunicacion.listar('clases', filtros)
    return {'asignaturas': asignaturas, 'clases': clases}

def mostrar_registros(self, datos):
    asignaturas = datos['asignaturas']
    self.asignaturas = {asignatura['nombre']: asignatura['id'] for asignatura in asignaturas}
    nombres = list(self.asignaturas)
    self.combo_asignatura.config(values=nombres)
    self.combo_filtro.config(values=[TODAS] + nombres)

    if self.id_filtro is None:
        total_horas = sum(asignatura['total_horas'] for asignatura in asignaturas)
    else:
        filtrada = [a for a in asignaturas if a['id'] == self.id_filtro]
        if not filtrada:
            self.filtro.set(TODAS)
            self.id_filtro = None
            self.refrescar()
            return
        self.filtro.set(filtrada[0]['nombre'])
        total_horas = filtrada[0]['total_horas']

    clases = datos['clases']
    self.label_total.config(
        text=str(len(clases)) + ' clases, ' + format(total_horas, 'g') + ' horas'
    )
    super().mostrar_registros(clases)

def validar(self):
    errores = Validaciones.validarClase(self.modelo)
    nombre = self.modelo.asignatura.get()
    if nombre and nombre not in self.asignaturas:
        errores.append('Asignatura: ya no existe. Consulte de nuevo.')
    return errores

def datos_formulario(self):
    id_asignatura = self.asignaturas[self.modelo.asignatura.get()]
    return self.modelo.a_diccionario(id_asignatura)

def crear_botones_extra(self, marco):
    self.filtro = tk.StringVar(self, value=TODAS)
    etiqueta = ttk.Label(marco, text='Ver clases de')
    self.combo_filtro = ttk.Combobox(marco, textvariable=self.filtro, state='readonly', width=24)
    self.label_total = ttk.Label(marco)

    etiqueta.pack(side='left', padx=(24, 6))
    self.combo_filtro.pack(side='left')
    self.label_total.pack(side='left', padx=12)

    self.combo_filtro.bind('<<ComboboxSelected>>', self.al_cambiar_filtro)

def al_cambiar_filtro(self, evento):
    self.id_filtro = self.asignaturas.get(self.filtro.get())
    self.refrescar()
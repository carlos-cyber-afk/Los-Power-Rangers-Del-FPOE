import tkinter as tk
import re
from datetime import datetime
import tkinter.messagebox as mesagebox
from tkcalendar import DateEntry
from libro import Libro
 
 
class Interfaz:
    def __init__(self):
        self.ventanaPrincipal = tk.Tk()
        self.libro = Libro(self.ventanaPrincipal)

    def validar_titulo(self, valor):
        valor = valor.strip()
        if valor == "":
            return "El título es obligatorio"
        if len(valor) > 100:
            return "Máximo 100 caracteres"
        patron = re.compile(r"^[A-Za-z0-9ñÑáéíóúÁÉÍÓÚüÜ .,:;¿?¡!'\-]+$")
        if patron.match(valor) is None:
            return "Hay caracteres no permitidos"
        return ""
 
    def validar_paginas(self, valor):
        if valor == "":
            return "El número de páginas es obligatorio"
        if re.match(r"^[0-9]+$", valor) is None:
            return "Solo se permiten números enteros"
        numero = int(valor)
        if numero < 1 or numero > 5000:
            return "Debe estar entre 1 y 5000"
        return ""
 
    def validar_fecha(self, valor):
        if re.match(r"^\d{2}/\d{2}/\d{4}$", valor) is None:
            return "Formato inválido (dd/mm/aaaa)"
        try:
            fecha = datetime.strptime(valor, "%d/%m/%Y")
        except ValueError:
            return "Esa fecha no existe"
        if fecha > datetime.now():
            return "La fecha no puede ser futura"
        return ""

    def evento_titulo(self, evento=None):
        mensaje = self.validar_titulo(self.libro.titulo.get())
        self.labelErrorTitulo.config(text=mensaje)
        return mensaje
 
    def evento_paginas(self, evento=None):
        mensaje = self.validar_paginas(self.libro.paginas.get())
        self.labelErrorPaginas.config(text=mensaje)
        return mensaje
 
    def evento_fecha(self, evento=None):
        mensaje = self.validar_fecha(self.libro.fecha_publicacion.get())
        self.labelErrorFecha.config(text=mensaje)
        return mensaje
 
    def accion_guardar_boton(self):
        errores = [
            self.evento_titulo(),
            self.evento_paginas(),
            self.evento_fecha(),
        ]
        if any(errores):
            mesagebox.showwarning("Datos inválidos", "Corrige los campos marcados en rojo.")
            return
 
        mesagebox.showinfo(
            "Guardar",
            f"Guardando: titulo: {self.libro.titulo.get().strip()}, "
            f"páginas: {self.libro.paginas.get()}, "
            f"fecha de publicación: {self.libro.fecha_publicacion.get()}, "
            f"disponible: {self.libro.disponible.get()}"
        )
 
    def mostrar_interfaz(self):
        # TITULO
        labelTitulo = tk.Label(self.ventanaPrincipal, text="Título")
        entryTitulo = tk.Entry(self.ventanaPrincipal, textvariable=self.libro.titulo)
        self.labelErrorTitulo = tk.Label(self.ventanaPrincipal, text="", fg="red")
 
        # PAGINAS
        labelPaginas = tk.Label(self.ventanaPrincipal, text="Número de páginas")
        spinPaginas = tk.Spinbox(
            self.ventanaPrincipal,
            from_=1,
            to=5000,
            textvariable=self.libro.paginas,
            command=self.evento_paginas  # valida al usar las flechas
        )
        self.labelErrorPaginas = tk.Label(self.ventanaPrincipal, text="", fg="red")
 
        # FECHA DE PUBLICACION
        labelFecha = tk.Label(self.ventanaPrincipal, text="Fecha de Publicación")
        date_fecha = DateEntry(
            self.ventanaPrincipal,
            textvariable=self.libro.fecha_publicacion,
            date_pattern='dd/mm/yyyy',
            locale='es_ES'
        )
        self.labelErrorFecha = tk.Label(self.ventanaPrincipal, text="", fg="red")
 
        # DISPONIBLE
        check = tk.Checkbutton(self.ventanaPrincipal, text="Disponible", variable=self.libro.disponible)
 
        boton_guardar = tk.Button(self.ventanaPrincipal, text="Guardar", command=self.accion_guardar_boton)
 
        # EVENTOS
        entryTitulo.bind("<KeyRelease>", self.evento_titulo)
        spinPaginas.bind("<KeyRelease>", self.evento_paginas)
        date_fecha.bind("<KeyRelease>", self.evento_fecha)
        date_fecha.bind("<<DateEntrySelected>>", self.evento_fecha)
 
        # VENTANA
        self.ventanaPrincipal.title("Ventana Principal")
        self.ventanaPrincipal.geometry("320x360")
        labelTitulo.pack()
        entryTitulo.pack()
        self.labelErrorTitulo.pack()
        labelPaginas.pack()
        spinPaginas.pack()
        self.labelErrorPaginas.pack()
        labelFecha.pack()
        date_fecha.pack()
        self.labelErrorFecha.pack()
        check.pack()
        boton_guardar.pack(pady=10)
 
        self.ventanaPrincipal.mainloop()
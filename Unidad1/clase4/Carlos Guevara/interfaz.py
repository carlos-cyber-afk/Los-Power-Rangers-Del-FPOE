import tkinter as tk
import tkinter.messagebox as mesagebox
from tkcalendar import DateEntry
from libro import Libro

class Interfaz:
    def __init__(self):
        self.ventanaPrincipal = tk.Tk()

    def accion_guardar_boton(self, titulo, paginas, fecha_publicacion, disponible):
        mesagebox.showinfo("Guardar", f"Guardando: titulo: {titulo}, páginas: {paginas}, fecha de publicación: {fecha_publicacion}, disponible: {disponible}")

    def mostrar_interfaz(self):
        libro = Libro(self.ventanaPrincipal)

        #TITULO
        labelTitulo = tk.Label(self.ventanaPrincipal, text="Título")
        entryTitulo = tk.Entry(self.ventanaPrincipal, textvariable=libro.titulo)

        #PAGINAS
        labelPaginas = tk.Label(self.ventanaPrincipal, text="Número de páginas")
        spinPaginas = tk.Spinbox(self.ventanaPrincipal, from_=1, to=5000, textvariable=libro.paginas)

        #FECHA DE PUBLICACION
        labelFecha = tk.Label(self.ventanaPrincipal, text="Fecha de Publicación")
        date_fecha = DateEntry(
            self.ventanaPrincipal, 
            textvariable=libro.fecha_publicacion, 
            date_pattern='dd/mm/yyyy',
            locale='es_ES'
        )

        #DISPONIBLE
        check = tk.Checkbutton(self.ventanaPrincipal, text="Disponible", variable=libro.disponible)

        boton_guardar = tk.Button(self.ventanaPrincipal,
                                   text="Guardar",
                                     command=lambda: self.accion_guardar_boton(libro.titulo.get(), libro.paginas.get(), libro.fecha_publicacion.get(), libro.disponible.get()))

        self.ventanaPrincipal.title("Ventana Principal")
        self.ventanaPrincipal.geometry("300x300")
        labelTitulo.pack()
        entryTitulo.pack()
        labelPaginas.pack()
        spinPaginas.pack()
        labelFecha.pack()
        date_fecha.pack()
        check.pack()
        boton_guardar.pack()
        
        self.ventanaPrincipal.mainloop()

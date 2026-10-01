import tkinter as tk
import tkinter.messagebox as messagebox
from Unidad1.JuanCamiloArenasGuiterrez.clase4.uva import Uva

class Interfaz():

    def __init__(self):

        self.ventana_principal = tk.Tk()

    def accion_guardar_boton(self,textura):
        messagebox.showinfo("guardar", f"Guardando: Textura: {textura}")

    def mostrar_interfaz(self):

        uva = Uva(self.ventana_principal)

        label_textura = tk.Label(self.ventana_principal, text="textura")
        entry_textura = tk.Entry(self.ventana_principal, textvariable=uva.textura)  

        boton_guardar = tk.Button(self.ventana_principal, text="Guardar", command=lambda: self.accion_guardar_boton(entry_textura.get()))

        self.ventana_principal.title("Ventana Principal")
        self.ventana_principal.geometry("300x300")
        label_textura.pack()
        entry_textura.pack()
        boton_guardar.pack()

        self.ventana_principal.mainloop()
        
import tkinter as tk
import re
import tkinter.messagebox as messagebox
from uva import Uva

class Interfaz():

    def __init__(self):

        self.ventana_principal = tk.Tk()

    def accion_guardar_boton(self,textura,peso,forma,tamaño):
        messagebox.showinfo("guardar", f"Guardando: Textura: {textura}, Peso: {peso}, Forma: {forma}, Tamaño: {tamaño}")


    def mostrar_interfaz(self):

        uva = Uva(self.ventana_principal)

        label_textura = tk.Label(self.ventana_principal, text="textura")
        entry_textura = tk.Entry(self.ventana_principal, textvariable=uva.textura)  
        label_peso = tk.Label(self.ventana_principal, text="peso")
        entry_peso = tk.Entry(self.ventana_principal, textvariable=uva.peso)
        label_forma = tk.Label(self.ventana_principal, text="forma")
        entry_forma = tk.Entry(self.ventana_principal, textvariable=uva.forma)
        label_tamaño = tk.Label(self.ventana_principal, text="tamaño")
        entry_tamaño = tk.Entry(self.ventana_principal, textvariable=uva.tamaño)
       

        boton_guardar = tk.Button(self.ventana_principal, text="Guardar", command=lambda: self.accion_guardar_boton(entry_textura.get(),
                                                                                     entry_peso.get(), entry_forma.get(), entry_tamaño.get()))

        

        self.ventana_principal.title("Ventana Principal")
        self.ventana_principal.geometry("300x300")
        label_textura.pack()
        entry_textura.pack()
        label_peso.pack()
        entry_peso.pack()
        label_forma.pack()
        entry_forma.pack()
        label_tamaño.pack()
        entry_tamaño.pack()
        boton_guardar.pack()
    

        self.ventana_principal.mainloop()
        
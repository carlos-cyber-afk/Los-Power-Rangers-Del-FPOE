import tkinter as tk
import re
from datetime import datetime
import tkinter.messagebox as messagebox
from uva import Uva


import tkinter as tk
import re
import tkinter.messagebox as messagebox
from uva import Uva



class Interfaz():

    def __init__(self):

        self.ventana_principal = tk.Tk()
        self.uva = Uva(self.ventana_principal)
        self.uva.peso = tk.StringVar(value="") 

    def validar_textura(self, valor):

        valor = valor.strip()
        if valor == "":
            return "no puede estar vacío"
        if len(valor) > 50:
            return "Máximo 50 caracteres"
        patron = re.compile(r"^[A-Za-zñÑáéíóúÁÉÍÓÚüÜ\s]+$")
        if patron.match(valor) is None:
            return "solo se permiten letras"
        return ""
    
    def validar_forma(self, valor):
            valor = valor.strip()
            if valor == "":
                return "no puede estar vacío"
            if len(valor) > 50:
                return "Máximo 50 caracteres"
            patron = re.compile(r"^[A-Za-zñÑáéíóúÁÉÍÓÚüÜ\s]+$")
            if patron.match(valor) is None:
               return "solo se permiten letras"
            return ""  
     
    def validar_peso(self, valor):
      valor = valor.strip()
      if valor == "":
          return "no puede estar vacío"
      try:
            valor_float = float(valor)
            if valor_float <= 0:
                return "Debe ser un número positivo"
      except ValueError:
            return "Debe ser un números"
      return ""

    def evento_textura(self, evento=None):
            mensaje = self.validar_textura(self.uva.textura.get())
            self.labelErrortextura.config(text=mensaje)
            return mensaje
     
    def evento_forma(self, evento=None):
            mensaje = self.validar_forma(self.uva.forma.get())
            self.labelErrorForma.config(text=mensaje)
            return mensaje
     
    def evento_peso(self, evento=None):
            mensaje = self.validar_peso(self.uva.peso.get())
            self.labelErrorpeso.config(text=mensaje)
            return mensaje
     
    def accion_guardar_boton(self):
            errores = [
                self.evento_textura(),
                self.evento_forma(),
                self.evento_peso(),
            ]
            if any(errores):
                messagebox.showerror("Error", "Hay errores en el formulario")
                return
             
             
            messagebox.showinfo(
                "guardar", 
               f"Guardando:\n"
               f"Textura: {self.uva.textura.get().strip()}\n" 
               f"Peso:{self.uva.peso.get().strip()} gr\n"
               f"Forma: {self.uva.forma.get().strip()}\n"
               f"Tamaño : {self.uva.tamaño.get()}")


    def mostrar_interfaz(self):


        uva = Uva(self.ventana_principal)

        #TEXTURA
        label_textura = tk.Label(self.ventana_principal, text="textura (suave/gruesa)")
        entry_textura = tk.Entry(self.ventana_principal, textvariable=uva.textura)
        self.labelErrortextura = tk.Label(self.ventana_principal, text="", fg="red")
        #PESO
        label_peso = tk.Label(self.ventana_principal, text="Peso (gr)")
        entry_peso = tk.Entry(self.ventana_principal, textvariable=uva.peso)
        self.labelErrorpeso = tk.Label(self.ventana_principal, text="", fg="red")
        #FORMA
        label_forma = tk.Label(self.ventana_principal, text="forma")
        entry_forma = tk.Entry(self.ventana_principal, textvariable=uva.forma)
        self.labelErrorForma = tk.Label(self.ventana_principal, text="", fg="red")
        #TAMAÑO
        label_tamaño = tk.Label(self.ventana_principal, text="tamaño rango 1-10")
        scale_tamaño = tk.Scale(self.ventana_principal, from_=1, to=10, orient="horizontal", variable=uva.tamaño)


        boton_guardar = tk.Button(
            self.ventana_principal,
            text="Guardar",
            command=self.accion_guardar_boton
        )

        entry_textura.bind("<KeyRelease>", self.evento_textura)
        entry_textura.bind("<FocusOut>", self.evento_textura)

        entry_peso.bind("<KeyRelease>", self.evento_peso)
        entry_peso.bind("<FocusOut>", self.evento_peso)

        entry_forma.bind("<KeyRelease>", self.evento_forma)
        entry_forma.bind("<FocusOut>", self.evento_forma)

        self.ventana_principal.title("Ventana Principal")
        self.ventana_principal.geometry("300x300")
        label_textura.pack()
        entry_textura.pack()
        self.labelErrortextura.pack()
        label_peso.pack()
        entry_peso.pack()
        self.labelErrorpeso.pack()
        label_forma.pack()
        entry_forma.pack()
        self.labelErrorForma.pack()
        label_tamaño.pack()
        scale_tamaño.pack()
        boton_guardar.pack(pady=15)

        self.ventana_principal.mainloop()
        


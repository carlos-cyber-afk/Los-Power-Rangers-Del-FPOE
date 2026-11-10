import tkinter as tk
import re

texto_validar_nombre = ""

ventanaPrincipal = tk.Tk()
nombre = tk.StringVar(ventanaPrincipal)
labelNombre = tk.Label(ventanaPrincipal, text = "nombre")
entryNombre = tk.Entry(ventanaPrincipal, textvariable=nombre)
labelValidacionNombre = tk.Label(ventanaPrincipal, text="")


def validarLetras(valor):
    patron = re.compile("^[A-Za-zñÑ\s]+$")
    resultado = patron.match(valor.get())
    if not resultado:
        return False
    return True


def evento_presionar_tecla(evento):
    global texto_validar_nombre
    global nombre
    if validarLetras(nombre):
        texto_validar_nombre = ""
    else:
        texto_validar_nombre = "Solo se permiten letras"
    labelValidacionNombre.config(text=texto_validar_nombre)


# Creando la ventana
ventanaPrincipal.title("Ventana Principal")
ventanaPrincipal.geometry("300x300")
labelNombre.pack()
entryNombre.bind("<KeyRelease>", evento_presionar_tecla)
entryNombre.pack()
labelValidacionNombre.pack()

ventanaPrincipal.mainloop()
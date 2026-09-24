from tkinter import Frame, Tk
from tkinter.messagebox import askyesno

principal = Tk()

principal.title("prueba de evento")

def digitar_Letra(event):

    print("digistaste la letra", repr(event.char))

def Click_izquierda(event):
    frame.focus_set()
    print("Clickeando en: ", event.x, event.y)

def el_usuario_quiere_salir():
    if askyesno("salir de la aplicacion ", "¿Estás seguro de que quieres salir?"):
        principal.destroy()

frame = Frame(principal, width=500, height=500)
frame.bind("<Key>", digitar_Letra)
frame.bind("<Button-1>", Click_izquierda)
frame.pack()
frame.focus_set()

principal.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)
principal.mainloop()


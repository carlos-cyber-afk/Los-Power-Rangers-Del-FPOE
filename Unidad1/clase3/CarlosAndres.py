from tkinter import Frame, Tk
from tkinter.messagebox import askyesno

principal = Tk()
principal.title("Los Power Rangers Del FPOE")

def digitar_letra(evento):
    print("digitaste la letra: ", evento.char)

def click_izquierdo(evento):
    frame.focus_set()
    print("clickeado en: ", evento.x, evento.y)

def el_usuario_quiere_salir():
    if askyesno("Salir de la aplicacion", "¿estas seguro de salir del programa?"):
        principal.destroy()

frame = Frame(principal, width=500, height=500)
frame.focus_set()
frame.bind("<Key>", digitar_letra)
frame.bind("<Button-1>", click_izquierdo)
frame.pack()

principal.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)
principal.mainloop()
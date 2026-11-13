import re
from datetime import datetime


class Validaciones():

    @staticmethod
    def validarTitulo(valor):
        texto = valor.strip()
        if not texto:
            return 'Título: falta este dato.'
        if len(texto) > 150:
            return 'Título: admite máximo 150 caracteres.'
        if not re.fullmatch(r"[A-Za-z0-9ñÑáéíóúÁÉÍÓÚüÜ .,:;¿?¡!'\-]+", texto):
            return 'Título: hay caracteres no permitidos.'
        return None

    @staticmethod
    def validarPaginas(valor):
        texto = valor.strip()
        if not texto:
            return 'Páginas: falta este dato.'
        if not re.fullmatch('[0-9]+', texto) or not 1 <= int(texto) <= 5000:
            return 'Páginas: debe ser un entero entre 1 y 5000.'
        return None

    @staticmethod
    def validarFechaPublicacion(valor):
        try:
            fecha = datetime.strptime(valor.strip(), '%d/%m/%Y')
        except ValueError:
            return 'Fecha de publicación: use el formato dd/mm/aaaa y una fecha que exista.'
        if fecha > datetime.now():
            return 'Fecha de publicación: no puede ser futura.'
        return None

    @staticmethod
    def validarLibro(libro):
        errores = [
            Validaciones.validarTitulo(libro.titulo.get()),
            Validaciones.validarPaginas(libro.paginas.get()),
            Validaciones.validarFechaPublicacion(libro.fecha_publicacion.get()),
        ]
        return [error for error in errores if error]
import re
from datetime import datetime


class Validaciones():

    @staticmethod
    def validarTitulo(valor):
        texto = valor.strip()
        if not texto:
            return 'esta casilla no puede estar vacía.'
        if len(texto) > 100:
            return 'Se admite máximo 100 caracteres.'
        if not re.fullmatch(r"[A-Za-z0-9ñÑáéíóúÁÉÍÓÚüÜ .,:;¿?¡!'\-]+", texto):
            return 'hay caracteres no permitidos.'
        return None

    @staticmethod
    def validarPaginas(valor):
        texto = valor.strip()
        if not texto:
            return 'esta casilla no puede estar vacía.'
        if not re.fullmatch('[0-9]+', texto) or not 1 <= int(texto) <= 5000:
            return 'no se pueden ingresar números negativos y mayores a 5000.'
        return None

    @staticmethod
    def validarFechaPublicacion(valor):
        try:
            fecha = datetime.strptime(valor.strip(), '%d/%m/%Y')
        except ValueError:
            return 'solo se admite el formato dd/mm/aaaa.'
        if fecha > datetime.now():
            return 'la fecha no puede ser futura.'
        return None

    @staticmethod
    def validarLibro(libro):
        errores = [
            Validaciones.validarTitulo(libro.titulo.get()),
            Validaciones.validarPaginas(libro.paginas.get()),
            Validaciones.validarFechaPublicacion(libro.fecha_publicacion.get()),
        ]
        return [error for error in errores if error]
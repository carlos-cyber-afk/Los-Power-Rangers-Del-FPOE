import re
from datetime import datetime


class Validaciones():

    @staticmethod
    def validarTextura(valor, campo, maximo):
        textura = valor.strip()
        maximo = int(100)
        if not textura:
            return campo + ': falta este dato.'
        if len(textura) > maximo:
            return campo + ': admite máximo ' + str(maximo) + ' caracteres.'
        return None

    @staticmethod
    def validarForma(valor, campo, maximo):
        forma = valor.strip()
        maximo = int(100)
        if not forma:
            return campo + ': falta este dato.'
        if len(forma) > maximo:
            return campo + ': admite máximo ' + str(maximo) + ' caracteres.'
        return None

    @staticmethod
    def validarTamaño(valor, campo, minimo, maximo):
        texto = valor.strip()
        minimo = int(1)
        maximo = int(10)
        if not re.fullmatch('[0-9]+', texto) or not minimo <= int(texto) <= maximo:
            return campo + ': debe ser un entero entre ' + str(minimo) + ' y ' + str(maximo) + '.'
        return None

    @staticmethod
    def validarPeso(valor, campo, minimo, maximo):
        texto = valor.strip()
        minimo = float(0.1)
        maximo = float(15.0)
        if not re.fullmatch('[0-9]+(?:\.[0-9]+)?', texto) or not minimo <= float(texto) <= maximo:
            return campo + ': debe ser un número entre ' + str(minimo) + ' y ' + str(maximo) + '    .'
        return None

    @staticmethod
    def validarUva(uva):
        errores = [
            Validaciones.validarTextura(uva.textura.get(), 'Textura', 100),
            Validaciones.validarForma(uva.forma.get(), 'Forma', 100),
            Validaciones.validarTamaño(uva.tamaño.get(), 'Tamaño', 1, 100),
            Validaciones.validarPeso(uva.peso.get(), 'Peso', 0.1, 15.0),
        ]
        return [error for error in errores if error]
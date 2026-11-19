import re


class Validaciones():

    @staticmethod
    def _validarTexto(valor, campo, maximo):
        texto = valor.strip()
        if not texto:
            return campo + ': falta este dato.'
        if len(texto) > maximo:
            return campo + ': admite máximo ' + str(maximo) + ' caracteres.'
        return None

    @staticmethod
    def validarTextura(valor, campo, maximo):
        return Validaciones._validarTexto(valor, campo, maximo)

    @staticmethod
    def validarForma(valor, campo, maximo):
        return Validaciones._validarTexto(valor, campo, maximo)

    @staticmethod
    def validarTamaño(valor, campo, minimo, maximo):
        texto = valor.strip()
        if not re.fullmatch(r'[0-9]+', texto) or not minimo <= int(texto) <= maximo:
            return campo + ': debe ser un entero entre ' + str(minimo) + ' y ' + str(maximo) + '.'
        return None

    @staticmethod
    def validarPeso(valor, campo, minimo, maximo):
        texto = valor.strip()
        # Se acepta coma o punto como separador decimal
        if not re.fullmatch(r'[0-9]+(?:[.,][0-9]+)?', texto) \
                or not minimo <= float(texto.replace(',', '.')) <= maximo:
            return campo + ': debe ser un número entre ' + str(minimo) + ' y ' + str(maximo) + '.'
        return None

    @staticmethod
    def validarUva(uva):
        errores = [
            Validaciones.validarTextura(uva.textura.get(), 'Textura', 100),
            Validaciones.validarForma(uva.forma.get(), 'Forma', 100),
            Validaciones.validarTamaño(uva.tamaño.get(), 'Tamaño', 1, 10),
            Validaciones.validarPeso(uva.peso.get(), 'Peso', 0.1, 15.0),
        ]
        return [error for error in errores if error]

    @staticmethod
    def validarClase(clase):
        errores = [
            None if clase.uva.get().strip() else 'Uva: seleccione una.',
            Validaciones.validarForma(clase.forma.get(), 'Forma', 100),
            Validaciones.validarTextura(clase.textura.get(), 'Textura', 100),
            Validaciones.validarTamaño(clase.tamaño.get(), 'Tamaño', 1, 10),
            Validaciones.validarPeso(clase.peso.get(), 'Peso', 0.1, 15.0),
            None if clase.modalidad.get() in clase.MODALIDADES
            else 'Modalidad: elija ' + ' o '.join(clase.MODALIDADES) + '.',
        ]
        return [error for error in errores if error]
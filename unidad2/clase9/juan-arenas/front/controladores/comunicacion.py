import requests

class ErrorComunicacion(Exception):
    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.codigo = codigo
    """Error con un mensaje listo para mostrarle al usuario."""

class Comunicacion():

    def __init__(self):
        self.url = 'http://localhost:8000/api/'

    def peticion(self, metodo, ruta, datos=None):
        try:
            resultado = requests.request(metodo, self.url + ruta, json=datos, timeout=5)
        except requests.RequestException:
            raise ErrorComunicacion(
                'No se pudo conectar con el servidor. ¿Está corriendo el back?'
            )
        if not resultado.ok:
            raise ErrorComunicacion(self.mensaje_error(resultado), resultado.status_code)
        return resultado.json() if resultado.content else None

    def mensaje_error(self, resultado):
        try:
            errores = resultado.json()
        except ValueError:
            return 'El servidor respondió con error ' + str(resultado.status_code) + '.'

        mensajes = []
        for campo, detalle in errores.items():
            texto = ' '.join(detalle) if isinstance(detalle, list) else str(detalle)
            if campo in ('detail', 'non_field_errors'):
                mensajes.append(texto)
            else:
                mensajes.append(campo + ': ' + texto)
        return '\n'.join(mensajes)

    def _ruta(self, recurso, id=None):
        # DRF exige la barra final: /api/uvas/ y /api/uvas/5/
        if id is None:
            return recurso + '/'
        return recurso + '/' + str(id) + '/'

    def listar(self, recurso):
        return self.peticion('GET', self._ruta(recurso))

    def consultar(self, recurso, id):
        return self.peticion('GET', self._ruta(recurso, id))

    def crear(self, recurso, datos):
        return self.peticion('POST', self._ruta(recurso), datos)

    def reemplazar(self, recurso, id, datos):
        return self.peticion('PUT', self._ruta(recurso, id), datos)

    def modificar(self, recurso, id, datos):
        return self.peticion('PATCH', self._ruta(recurso, id), datos)

    def eliminar(self, recurso, id):
        return self.peticion('DELETE', self._ruta(recurso, id))

    def guardar(self, recurso, datos, id=None):
        if id is None:
            return self.crear(recurso, datos)
        return self.reemplazar(recurso, id, datos)
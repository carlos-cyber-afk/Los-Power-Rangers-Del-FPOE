import requests


class ErrorComunicacion(Exception):

    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.codigo = codigo


class Comunicacion:

    def __init__(self, base='http://127.0.0.1:8000/api/'):
        self.base = base

    def _url(self, recurso, id=None):
        if id is None:
            return f'{self.base}{recurso}/'
        return f'{self.base}{recurso}/{id}/'

    def _enviar(self, metodo, url, **kwargs):
        try:
            respuesta = requests.request(metodo, url, timeout=10, **kwargs)
        except requests.exceptions.RequestException:
            raise ErrorComunicacion('No se pudo conectar con el servidor')

        if respuesta.status_code >= 400:
            raise ErrorComunicacion(respuesta.text, respuesta.status_code)

        if respuesta.status_code == 204:
            return None
        return respuesta.json()

    def listar(self, recurso):
        return self._enviar('GET', self._url(recurso))

    def consultar(self, recurso, id):
        return self._enviar('GET', self._url(recurso, id))

    def crear(self, recurso, datos):
        return self._enviar('POST', self._url(recurso), json=datos)

    def reemplazar(self, recurso, id, datos):
        return self._enviar('PUT', self._url(recurso, id), json=datos)

    def modificar(self, recurso, id, cambios):
        return self._enviar('PATCH', self._url(recurso, id), json=cambios)

    def eliminar(self, recurso, id):
        return self._enviar('DELETE', self._url(recurso, id))
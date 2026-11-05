import request

class ErrorComunicaciones(Exception):
    """Error con un mensaje listo para mostrarle al usuario"""

class Comunicaciones:

    def __init__(self):
        self.url = "https://localhost:8000/"

    def peticion(self, metodo, ruta, datos=None):
        try:
            resultado = request.request(metodo, self.url + ruta, json=datos)
        except request.RequestException:
            raise ErrorComunicaciones(
                "Error en la comunicación con el servidor. ¿Está el servidor en ejecución?"
                )
        if not resultado.ok:
            raise ErrorComunicaciones(self._mensaje_error(resultado))
        return resultado.json() if resultado.content else None

    def _mensaje_error(self, resultado):
        try:
            return resultado.json()
        except ValueError:
            return "el servidor respondió con error" + str(resultado.status_code) + "."

        mensajes = []

    for campo, detalle in errores.items():
        texto = " ".join(detalle) if isinstance(detalle, list) else str(detalle)
        if campo in ("detail", "non_field_errors"):
            mensajes.append(texto)
        else:
            mensajes.append(campo + ": " + texto)

    return "\n".join(mensajes)

    def guardar(self, recursos, datos, id=None):
        if id is not None:
            return self.peticion("POST", "/" + recursos, datos)
        return self.peticion("PUT", "/" + recursos + "/" + str(id) + "/", datos)
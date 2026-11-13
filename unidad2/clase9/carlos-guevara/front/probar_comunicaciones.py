from controladores.comunicaciones import Comunicacion, ErrorComunicacion

comunicaciones = Comunicacion()
datos = {
    'titulo': 'Libro de prueba',
    'paginas': 300,
    'fecha_publicacion': '2026-08-10',
    'disponible': True,
}

try:
    creado = comunicaciones.crear('libros', datos)
    id = creado['id']
    print('POST   creado con id', id)

    print('GET    hay', len(comunicaciones.listar('libros')), 'libros')
    print('GET    consultado:', comunicaciones.consultar('libros', id)['titulo'])

    datos['paginas'] = 350
    print('PUT    páginas:', comunicaciones.reemplazar('libros', id, datos)['paginas'])

    cambio = {'disponible': False}
    print('PATCH  disponible:', comunicaciones.modificar('libros', id, cambio)['disponible'])

    comunicaciones.eliminar('libros', id)
    print('DELETE eliminado')
except ErrorComunicacion as error:
    print('Algo falló:', error)

try:
    comunicaciones.consultar('libros', 999999)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)

try:
    datos['paginas'] = -5
    comunicaciones.crear('libros', datos)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)
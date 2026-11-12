import os
import sys

# Permite ejecutarlo desde cualquier carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controladores.comunicacion import Comunicacion, ErrorComunicacion

comunicacion = Comunicacion()
datos ={
    "peso": 12.5,
    "tamano": 8,
    "forma": "Redonda",
    "textura": "crujiente"
}

try:
    creada = comunicacion.crear('uvas', datos)
    id = creada['id']
    print('POST   creada con id', id)

    print('GET    hay', len(comunicacion.listar('uvas')), 'uvas')
    print('GET    consultada (tamaño):', comunicacion.consultar('uvas', id)['tamano'])

    datos['peso'] = 14.0
    print('PUT    peso actualizado:', comunicacion.reemplazar('uvas', id, datos)['peso'])

    cambio = {'textura': 'Rugosa'}
    print('PATCH  textura modificada:', comunicacion.modificar('uvas', id, cambio)['textura'])

    comunicacion.eliminar('uvas', id)
    print('DELETE eliminada')
except ErrorComunicacion as error:
    print('Algo falló:', error)

try:
    comunicacion.consultar('uvas', 999999)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)

try:
    datos['peso'] = 99  # valor inválido: el back lo rechaza con 400
    comunicacion.crear('uvas', datos)
except ErrorComunicacion as error:
    print('Código', error.codigo, '->', error)
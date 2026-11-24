// Cliente centralizado: TODAS las peticiones al backend pasan por aquí.
// Usa los cinco verbos: GET, POST, PUT, PATCH y DELETE.
const BASE = '/api' // el proxy de Vite lo manda a Django (ver vite.config.js)

export class ErrorApi extends Error {
  constructor(estado, mensaje, datos = null) {
    super(mensaje)
    this.estado = estado // 0 = no hubo conexión
    this.datos = datos
  }
}

// Convierte lo que responde Django en un mensaje entendible
function mensajeDeError(estado, datos) {
  if (estado === 400 && datos) {
    if (typeof datos === 'string') return datos
    if (Array.isArray(datos)) return datos.join(' ')
    return Object.entries(datos)
      .map(([campo, errores]) => {
        const texto = [].concat(errores).join(' ')
        return campo === 'non_field_errors' || campo === 'detail' ? texto : `${campo}: ${texto}`
      })
      .join(' · ')
  }
  if (estado === 404) return 'Ese registro ya no existe.'
  if (estado === 409) return 'Este producto ya tiene ventas y no se puede eliminar. Retíralo de la venta en su lugar.'
  return `El servidor respondió con un error (código ${estado}).`
}

async function peticion(metodo, ruta, cuerpo) {
  let respuesta
  try {
    respuesta = await fetch(BASE + ruta, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: cuerpo ? JSON.stringify(cuerpo) : undefined,
    })
  } catch {
    throw new ErrorApi(0, 'No hay conexión con el servidor. Revisa que el backend esté encendido.')
  }

  if (respuesta.status === 204) return null // DELETE exitoso: sin contenido

  let datos = null
  try {
    datos = await respuesta.json()
  } catch {
    /* la respuesta no traía JSON */
  }

  if (!respuesta.ok) throw new ErrorApi(respuesta.status, mensajeDeError(respuesta.status, datos), datos)
  return datos
}

// Funciona con o sin paginación de DRF
const lista = (datos) => datos.results ?? datos

export const api = {
  productos: {
    listar: async () => lista(await peticion('GET', '/productos/')),
    crear: (producto) => peticion('POST', '/productos/', producto), // 201
    editar: (id, producto) => peticion('PUT', `/productos/${id}/`, producto), // 200, objeto completo
    cambiarActivo: (id, activo) => peticion('PATCH', `/productos/${id}/`, { activo }), // 200, solo un campo
    eliminar: (id) => peticion('DELETE', `/productos/${id}/`), // 204 o 409
  },
  ventas: {
    listar: async () => lista(await peticion('GET', '/ventas/')),
    crear: (venta) => peticion('POST', '/ventas/', venta), // 201
    eliminar: (id) => peticion('DELETE', `/ventas/${id}/`), // 204
  },
  detalles: {
    listar: async (ventaId) => {
      // Si no hay ventaId o es indefinido, no hace la petición y retorna lista vacía
      if (!ventaId) return [] 
      return lista(await peticion('GET', `/detalles/?venta=${ventaId}`))
    },
    crear: (detalle) => peticion('POST', '/detalles/', detalle), // 201
    eliminar: (id) => peticion('DELETE', `/detalles/${id}/`), // 204
  },
}
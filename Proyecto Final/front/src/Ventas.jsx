import { useEffect, useState } from 'react'
import { api } from './Api'
import './Ventas.css'

const pesos = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  maximumFractionDigits: 2,
})

const METODOS = [
  { valor: 'EFECTIVO', texto: 'Efectivo' },
  { valor: 'TARJETA', texto: 'Tarjeta' },
  { valor: 'TRANSFERENCIA', texto: 'Transferencia' },
]

const FORM_VACIO = { cliente: '', metodo_pago: 'EFECTIVO', observaciones: '' }
const DETALLE_VACIO = { producto: '', cantidad: '1' }

function formatearFecha(texto) {
  return new Date(texto).toLocaleString('es-CO', { dateStyle: 'short', timeStyle: 'short' })
}

function Ventas() {
  const [ventas, setVentas] = useState([])
  const [productos, setProductos] = useState([])
  const [detalles, setDetalles] = useState([])
  const [seleccionada, setSeleccionada] = useState(null)
  
  const [form, setForm] = useState(FORM_VACIO)
  const [formDetalle, setFormDetalle] = useState(DETALLE_VACIO)
  
  // Estados de errores específicos por campo
  const [erroresVenta, setErroresVenta] = useState({})
  const [erroresDetalle, setErroresDetalle] = useState({})

  const [aviso, setAviso] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [enviando, setEnviando] = useState(false)

  const venta = ventas.find((v) => v.id === seleccionada)
  const disponibles = productos.filter((p) => p.activo && p.stock > 0)
  const nombreDe = (d) => d.producto_nombre ?? productos.find((p) => p.id === d.producto)?.nombre ?? `Producto #${d.producto}`

  const cargarVentas = async () => setVentas(await api.ventas.listar())
  const cargarProductos = async () => setProductos(await api.productos.listar())
  const cargarDetalles = async (id) => {
    if (!id) return setDetalles([])
    const datos = await api.detalles.listar(id)
    setDetalles(datos)
  }

  const mostrarError = (err) => setAviso({ tipo: 'error', texto: err.message })

  useEffect(() => {
    async function inicio() {
      try {
        await Promise.all([cargarVentas(), cargarProductos()])
      } catch (err) {
        mostrarError(err)
      } finally {
        setCargando(false)
      }
    }
    inicio()
  }, [])

  async function seleccionar(id) {
    setSeleccionada(id)
    setDetalles([])
    setFormDetalle(DETALLE_VACIO)
    setErroresDetalle({})
    setAviso(null)
    try {
      await cargarDetalles(id)
    } catch (err) {
      mostrarError(err)
    }
  }

  // Validación local del formulario Nueva Venta
  function validarVenta(f) {
    const errores = {}
    const letras = 'A-Za-zÁÉÍÓÚÜÑáéíóúüñ'
    const cliente = f.cliente.trim()

    if (!cliente) {
      errores.cliente = 'Escribe el nombre del cliente.'
    } else if (cliente.length < 2) {
      errores.cliente = 'El nombre del cliente debe tener al menos 2 caracteres.'
    } else if (!new RegExp(`^[${letras}0-9 .,()-]+$`).test(cliente) || !new RegExp(`[${letras}]`).test(cliente)) {
      errores.cliente = 'El nombre solo puede contener letras, números, espacios y . , - ( ), y al menos una letra.'
    }

    return errores
  }

  async function crearVenta(e) {
    e.preventDefault()
    setErroresVenta({})

    const errores = validarVenta(form)
    if (Object.keys(errores).length > 0) {
      setErroresVenta(errores)
      return
    }

    setEnviando(true)
    setAviso(null)
    try {
      const nueva = await api.ventas.crear({
        cliente: form.cliente.trim(),
        metodo_pago: form.metodo_pago,
        observaciones: form.observaciones.trim(),
      })
      setForm(FORM_VACIO)
      setErroresVenta({})
      await cargarVentas()
      await seleccionar(nueva.id)
      setAviso({ tipo: 'ok', texto: 'Venta creada. Ahora agrégale productos.' })
    } catch (err) {
      if (err.datos && typeof err.datos === 'object') {
        const errMap = {}
        Object.entries(err.datos).forEach(([k, v]) => { errMap[k] = Array.isArray(v) ? v.join(' ') : v })
        setErroresVenta(errMap)
      } else {
        mostrarError(err)
      }
    } finally {
      setEnviando(false)
    }
  }

  // Validación local del formulario Agregar Producto a Venta
  function validarDetalle(f) {
    const errores = {}
    if (!f.producto) {
      errores.producto = 'Debes elegir un producto.'
    }
    const cantidad = Number(f.cantidad)
    if (f.cantidad === '' || Number.isNaN(cantidad)) {
      errores.cantidad = 'Ingresa una cantidad válida.'
    } else if (!Number.isInteger(cantidad) || cantidad < 1) {
      errores.cantidad = 'La cantidad no puede ser menor que 1.'
    } else {
      const prod = productos.find((p) => p.id === Number(f.producto))
      if (prod && cantidad > prod.stock) {
        errores.cantidad = `Solo quedan ${prod.stock} de ${prod.nombre}.`
      }
    }
    return errores
  }

  async function agregarDetalle(e) {
    e.preventDefault()
    setErroresDetalle({})

    if (!seleccionada) return setAviso({ tipo: 'error', texto: 'No hay ninguna venta seleccionada.' })

    const errores = validarDetalle(formDetalle)
    if (Object.keys(errores).length > 0) {
      setErroresDetalle(errores)
      return
    }

    const producto = productos.find((p) => p.id === Number(formDetalle.producto))
    const cantidad = Number(formDetalle.cantidad)

    setEnviando(true)
    setAviso(null)
    try {
      await api.detalles.crear({
        venta: seleccionada,
        producto: producto.id,
        cantidad,
        precio_unitario: producto.precio,
      })
      setFormDetalle(DETALLE_VACIO)
      setErroresDetalle({})
      await Promise.all([cargarVentas(), cargarProductos(), cargarDetalles(seleccionada)])
      setAviso({ tipo: 'ok', texto: 'Producto agregado a la venta.' })
    } catch (err) {
      if (err.datos && typeof err.datos === 'object') {
        const errMap = {}
        Object.entries(err.datos).forEach(([k, v]) => { errMap[k] = Array.isArray(v) ? v.join(' ') : v })
        setErroresDetalle(errMap)
      } else {
        mostrarError(err)
      }
    } finally {
      setEnviando(false)
    }
  }

  async function eliminarVenta(v) {
    if (!window.confirm(`¿Eliminar la venta de ${v.cliente}? Se borrarán también sus productos.`)) return
    setAviso(null)
    try {
      await api.ventas.eliminar(v.id)
      if (seleccionada === v.id) {
        setSeleccionada(null)
        setDetalles([])
      }
      await Promise.all([cargarVentas(), cargarProductos()])
      setAviso({ tipo: 'ok', texto: 'Venta eliminada.' })
    } catch (err) {
      mostrarError(err)
    }
  }

  async function quitarDetalle(d) {
    setAviso(null)
    try {
      await api.detalles.eliminar(d.id)
      await Promise.all([cargarVentas(), cargarProductos(), cargarDetalles(seleccionada)])
      setAviso({ tipo: 'ok', texto: 'Producto quitado de la venta.' })
    } catch (err) {
      mostrarError(err)
    }
  }

  const detallesDeVentaElegida = detalles.filter((d) => d.venta === seleccionada || !d.venta)

  return (
    <main className="catalogo">
      <h1 className="catalogo-titulo">Ventas</h1>

      {aviso && (
        <p className={`aviso aviso-${aviso.tipo}`} role={aviso.tipo === 'error' ? 'alert' : 'status'}>
          {aviso.texto}
        </p>
      )}

      <div className="catalogo-cuerpo">
        {/* Formulario Nueva Venta */}
        <form className="tarjeta formulario" onSubmit={crearVenta} noValidate>
          <h2>Nueva venta</h2>

          <label htmlFor="cliente">Cliente</label>
          <input
            id="cliente"
            className={erroresVenta.cliente ? 'input-error' : ''}
            value={form.cliente}
            maxLength={100}
            onChange={(e) => {
              setForm({ ...form, cliente: e.target.value })
              if (erroresVenta.cliente) setErroresVenta({ ...erroresVenta, cliente: null })
            }}
          />
          {erroresVenta.cliente && (
            <span className="mensaje-error-campo">{erroresVenta.cliente}</span>
          )}

          <label htmlFor="metodo_pago">Forma de pago</label>
          <select
            id="metodo_pago"
            className={erroresVenta.metodo_pago ? 'input-error' : ''}
            value={form.metodo_pago}
            onChange={(e) => {
              setForm({ ...form, metodo_pago: e.target.value })
              if (erroresVenta.metodo_pago) setErroresVenta({ ...erroresVenta, metodo_pago: null })
            }}
          >
            {METODOS.map((m) => (
              <option key={m.valor} value={m.valor}>{m.texto}</option>
            ))}
          </select>
          {erroresVenta.metodo_pago && (
            <span className="mensaje-error-campo">{erroresVenta.metodo_pago}</span>
          )}

          <label htmlFor="observaciones">Observaciones (opcional)</label>
          <textarea
            id="observaciones"
            rows={3}
            value={form.observaciones}
            onChange={(e) => setForm({ ...form, observaciones: e.target.value })}
          />

          <div className="formulario-botones">
            <button className="btn btn-acento" type="submit" disabled={enviando}>
              Crear venta
            </button>
          </div>
        </form>

        {/* Tabla de ventas */}
        <div className="tarjeta tabla-caja">
          {cargando ? (
            <p className="vacio">Cargando ventas…</p>
          ) : ventas.length === 0 ? (
            <p className="vacio">Aún no hay ventas. Crea la primera con el formulario.</p>
          ) : (
            <table className="tabla">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Cliente</th>
                  <th>Pago</th>
                  <th className="num">Total</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {ventas.map((v) => (
                  <tr key={v.id} className={seleccionada === v.id ? 'editando' : ''}>
                    <td>{formatearFecha(v.fecha)}</td>
                    <td>{v.cliente}</td>
                    <td>{METODOS.find((m) => m.valor === v.metodo_pago)?.texto ?? v.metodo_pago}</td>
                    <td className="num">{pesos.format(v.total ?? 0)}</td>
                    <td>
                      <div className="acciones">
                        <button className="enlace" onClick={() => seleccionar(v.id)}>Ver productos</button>
                        <button className="enlace peligro" onClick={() => eliminarVenta(v)}>Eliminar</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Detalles de la venta seleccionada */}
      {venta && (
        <section className="tarjeta detalles">
          <h2>Productos de la venta de {venta.cliente}</h2>

          <form className="fila-detalle" onSubmit={agregarDetalle} noValidate>
            <div className="campo-producto">
              <label htmlFor="producto">Producto</label>
              <select
                id="producto"
                className={erroresDetalle.producto ? 'input-error' : ''}
                value={formDetalle.producto}
                onChange={(e) => {
                  setFormDetalle({ ...formDetalle, producto: e.target.value })
                  if (erroresDetalle.producto) setErroresDetalle({ ...erroresDetalle, producto: null })
                }}
              >
                <option value="">Elige un producto…</option>
                {disponibles.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.nombre} — {pesos.format(p.precio)} ({p.stock} disponibles)
                  </option>
                ))}
              </select>
              {erroresDetalle.producto && (
                <span className="mensaje-error-campo">{erroresDetalle.producto}</span>
              )}
            </div>

            <div className="campo-cantidad">
              <label htmlFor="cantidad">Cantidad</label>
              <input
                id="cantidad"
                type="number"
                min="1"
                step="1"
                className={erroresDetalle.cantidad ? 'input-error' : ''}
                value={formDetalle.cantidad}
                onChange={(e) => {
                  setFormDetalle({ ...formDetalle, cantidad: e.target.value })
                  if (erroresDetalle.cantidad) setErroresDetalle({ ...erroresDetalle, cantidad: null })
                }}
              />
              {erroresDetalle.cantidad && (
                <span className="mensaje-error-campo">{erroresDetalle.cantidad}</span>
              )}
            </div>

            <button className="btn btn-acento" type="submit" disabled={enviando}>
              Agregar
            </button>
          </form>

          {detallesDeVentaElegida.length === 0 ? (
            <p className="vacio">Esta venta aún no tiene productos.</p>
          ) : (
            <div className="tabla-caja">
              <table className="tabla">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th className="num">Cantidad</th>
                    <th className="num">Precio unitario</th>
                    <th className="num">Subtotal</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {detallesDeVentaElegida.map((d) => (
                    <tr key={d.id}>
                      <td>{nombreDe(d)}</td>
                      <td className="num">{d.cantidad}</td>
                      <td className="num">{pesos.format(d.precio_unitario)}</td>
                      <td className="num">{pesos.format(d.cantidad * d.precio_unitario)}</td>
                      <td>
                        <button className="enlace peligro" onClick={() => quitarDetalle(d)}>Quitar</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <p className="total">
            Total: <strong>{pesos.format(venta.total ?? 0)}</strong>
          </p>
        </section>
      )}
    </main>
  )
}

export default Ventas
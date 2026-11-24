import { useEffect, useState } from 'react'
import { api } from './Api'
import './Productos.css'

const FORM_VACIO = { nombre: '', precio: '', stock: '0' }

const pesos = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  maximumFractionDigits: 2,
})

// Devuelve un objeto con los errores por cada campo o {} si todo está bien
function validarCampos(f) {
  const errores = {}
  const letras = 'A-Za-zÁÉÍÓÚÜÑáéíóúüñ'
  const nombre = f.nombre.trim()

  if (!nombre) {
    errores.nombre = 'Escribe el nombre del producto.'
  } else if (!new RegExp(`^[${letras}0-9 .,()-]+$`).test(nombre) || !new RegExp(`[${letras}]`).test(nombre)) {
    errores.nombre = 'El nombre solo puede tener letras, números, espacios y . , - ( ), y al menos una letra.'
  }

  const precio = Number(f.precio)
  if (!f.precio || Number.isNaN(precio) || precio <= 0) {
    errores.precio = 'El precio debe ser mayor que cero.'
  }

  const stock = Number(f.stock)
  if (f.stock === '' || Number.isNaN(stock) || !Number.isInteger(stock) || stock < 0) {
    errores.stock = 'La existencia no puede ser menor que 0.'
  }

  return errores
}

function Productos() {
  const [productos, setProductos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [form, setForm] = useState(FORM_VACIO)
  const [editando, setEditando] = useState(null)
  const [aviso, setAviso] = useState(null)
  const [guardando, setGuardando] = useState(false)
  
  // Estado para controlar errores individuales por campo
  const [erroresCampos, setErroresCampos] = useState({})

  async function cargar() {
    try {
      setProductos(await api.productos.listar())
    } catch (err) {
      setAviso({ tipo: 'error', texto: err.message })
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    cargar()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function cambiarCampo(e) {
    const { name, value } = e.target
    setForm({ ...form, [name]: value })
    // Si el campo tenía un error, lo limpia al editar
    if (erroresCampos[name]) {
      setErroresCampos({ ...erroresCampos, [name]: null })
    }
  }

  function empezarEdicion(producto) {
    setEditando(producto)
    setForm({ nombre: producto.nombre, precio: String(producto.precio), stock: String(producto.stock) })
    setErroresCampos({})
    setAviso(null)
  }

  function cancelar() {
    setEditando(null)
    setForm(FORM_VACIO)
    setErroresCampos({})
  }

  async function guardar(e) {
    e.preventDefault()
    setErroresCampos({})

    const errores = validarCampos(form)
    if (Object.keys(errores).length > 0) {
      setErroresCampos(errores)
      return
    }

    const datos = {
      nombre: form.nombre.trim(),
      precio: Number(form.precio).toFixed(2),
      stock: Number(form.stock),
    }

    setGuardando(true)
    setAviso(null)
    try {
      if (editando) {
        await api.productos.editar(editando.id, { ...datos, activo: editando.activo })
        setAviso({ tipo: 'ok', texto: 'Producto actualizado.' })
      } else {
        await api.productos.crear({ ...datos, activo: true })
        setAviso({ tipo: 'ok', texto: 'Producto creado.' })
      }
      cancelar()
      await cargar()
    } catch (err) {
      if (err.datos && typeof err.datos === 'object') {
        const erroresBackend = {}
        Object.entries(err.datos).forEach(([campo, msgs]) => {
          erroresBackend[campo] = Array.isArray(msgs) ? msgs.join(' ') : msgs
        })
        setErroresCampos(erroresBackend)
      } else {
        setAviso({ tipo: 'error', texto: err.message })
      }
    } finally {
      setGuardando(false)
    }
  }

  async function alternarActivo(producto) {
    setAviso(null)
    try {
      await api.productos.cambiarActivo(producto.id, !producto.activo)
      setAviso({ tipo: 'ok', texto: producto.activo ? 'Producto retirado de la venta.' : 'Producto reactivado.' })
      await cargar()
    } catch (err) {
      setAviso({ tipo: 'error', texto: err.message })
    }
  }

  async function eliminar(producto) {
    if (!window.confirm(`¿Eliminar "${producto.nombre}"? Esta acción no se puede deshacer.`)) return
    setAviso(null)
    try {
      await api.productos.eliminar(producto.id)
      if (editando?.id === producto.id) cancelar()
      setAviso({ tipo: 'ok', texto: 'Producto eliminado.' })
      await cargar()
    } catch (err) {
      setAviso({ tipo: 'error', texto: err.message })
    }
  }

  return (
    <main className="catalogo">
      <h1 className="catalogo-titulo">Productos</h1>

      {aviso && (
        <p className={`aviso aviso-${aviso.tipo}`} role={aviso.tipo === 'error' ? 'alert' : 'status'}>
          {aviso.texto}
        </p>
      )}

      <div className="catalogo-cuerpo">
        {/* Formulario */}
        <form className="tarjeta formulario" onSubmit={guardar} noValidate>
          <h2>{editando ? 'Editar producto' : 'Nuevo producto'}</h2>

          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            name="nombre"
            className={erroresCampos.nombre ? 'input-error' : ''}
            value={form.nombre}
            onChange={cambiarCampo}
            maxLength={100}
          />
          {erroresCampos.nombre && (
            <span className="mensaje-error-campo">{erroresCampos.nombre}</span>
          )}

          <label htmlFor="precio">Precio (COP)</label>
          <input
            id="precio"
            name="precio"
            type="number"
            min="0"
            step="0.01"
            className={erroresCampos.precio ? 'input-error' : ''}
            value={form.precio}
            onChange={cambiarCampo}
          />
          {erroresCampos.precio && (
            <span className="mensaje-error-campo">{erroresCampos.precio}</span>
          )}

          <label htmlFor="stock">Existencias</label>
          <input
            id="stock"
            name="stock"
            type="number"
            min="0"
            step="1"
            className={erroresCampos.stock ? 'input-error' : ''}
            value={form.stock}
            onChange={cambiarCampo}
          />
          {erroresCampos.stock && (
            <span className="mensaje-error-campo">{erroresCampos.stock}</span>
          )}

          <div className="formulario-botones">
            <button className="btn btn-acento" type="submit" disabled={guardando}>
              {guardando ? 'Guardando…' : editando ? 'Guardar cambios' : 'Crear producto'}
            </button>
            {editando && (
              <button className="btn btn-claro" type="button" onClick={cancelar}>
                Cancelar
              </button>
            )}
          </div>
        </form>

        {/* Tabla */}
        <div className="tarjeta tabla-caja">
          {cargando ? (
            <p className="vacio">Cargando productos…</p>
          ) : productos.length === 0 ? (
            <p className="vacio">Aún no hay productos. Crea el primero con el formulario.</p>
          ) : (
            <table className="tabla">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th className="num">Precio</th>
                  <th className="num">Existencias</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {productos.map((p) => (
                  <tr key={p.id} className={editando?.id === p.id ? 'editando' : ''}>
                    <td>{p.nombre}</td>
                    <td className="num">{pesos.format(p.precio)}</td>
                    <td className="num">{p.stock}</td>
                    <td>
                      <span className={`etiqueta ${p.activo ? 'activo' : 'retirado'}`}>
                        {p.activo ? 'En venta' : 'Retirado'}
                      </span>
                    </td>
                    <td>
                      <div className="acciones">
                        <button className="enlace" onClick={() => empezarEdicion(p)}>Editar</button>
                        <button className="enlace" onClick={() => alternarActivo(p)}>
                          {p.activo ? 'Retirar' : 'Reactivar'}
                        </button>
                        <button className="enlace peligro" onClick={() => eliminar(p)}>Eliminar</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </main>
  )
}

export default Productos
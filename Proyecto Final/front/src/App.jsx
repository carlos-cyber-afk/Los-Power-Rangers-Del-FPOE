import { useState } from 'react'
import './App.css'
import Productos from './Productos'
import Ventas from './Ventas'
import Historial from './Historial'

const enlaces = [
  { texto: 'Inicio', vista: 'inicio' },
  { texto: 'Productos', vista: 'productos' },
  { texto: 'Ventas', vista: 'ventas' },
  { texto: 'Historial', vista: 'historial' },
]

// Dibujo de línea reutilizable para los íconos
function Icono({ children, tamano = 28 }) {
  return (
    <svg
      width={tamano}
      height={tamano}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  )
}

const caja = <path d="M3 7l9-4 9 4-9 4-9-4z M3 7v10l9 4 9-4V7 M12 11v10" />
const recibo = <path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3z M9 8h6 M9 12h6" />
const pin = (
  <>
    <path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z" />
    <circle cx="12" cy="10" r="2.5" />
  </>
)

function App() {
  // Qué pantalla se muestra: 'inicio', 'productos', 'ventas' o 'historial'
  const [vista, setVista] = useState('inicio')

  function ir(e, destino) {
    e.preventDefault() // evita que el enlace recargue la página
    setVista(destino)
  }

  return (
    <div className="app">
      <nav className="nav">
        <div className="logo">El Cafetal</div>
        <ul className="nav-links">
          {enlaces.map((enlace) => (
            <li key={enlace.vista}>
              <a
                href="#"
                onClick={(e) => ir(e, enlace.vista)}
                aria-current={vista === enlace.vista ? 'page' : undefined}
              >
                {enlace.texto}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {vista === 'productos' && <Productos />}
      {vista === 'ventas' && <Ventas />}
      {vista === 'historial' && <Historial />}

      {vista === 'inicio' && (
        <>
          <header className="hero">
            <div className="hero-foto" aria-hidden="true"></div>

            <div className="hero-texto">
              <h1>Comercializadora El Cafetal</h1>
              <p>Lleva el control de tus productos y tus ventas en un solo lugar.</p>
              <button className="btn btn-dorado" onClick={() => setVista('productos')}>
                Ir a Productos
              </button>
            </div>

            <aside className="hero-panel">
              <button className="panel-item" onClick={() => setVista('productos')}>
                <Icono>{caja}</Icono>
                <span>
                  <strong>Productos</strong>
                  <small>Registra cafés, precios y existencias.</small>
                </span>
              </button>

              <button className="panel-item" onClick={() => setVista('ventas')}>
                <Icono>{recibo}</Icono>
                <span>
                  <strong>Ventas</strong>
                  <small>Anota cada venta y mira el total al instante.</small>
                </span>
              </button>

              <div className="panel-item">
                <Icono>{pin}</Icono>
                <span>
                  <strong>Ubicación</strong>
                  <small>Caicedonia, Valle del Cauca</small>
                </span>
              </div>
            </aside>
          </header>

          <section className="franja">
            <div className="franja-texto">
              <Icono tamano={44}>{recibo}</Icono>
              <div>
                <strong>Registra tu próxima venta</strong>
                <span>El sistema calcula el total y descuenta las existencias.</span>
              </div>
            </div>
            <button className="btn btn-contorno" onClick={() => setVista('ventas')}>
              Ir a Ventas
            </button>
          </section>
        </>
      )}
    </div>
  )
}

export default App
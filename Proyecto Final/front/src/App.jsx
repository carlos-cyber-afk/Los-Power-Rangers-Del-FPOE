import './App.css'

const enlaces = ['Inicio', 'Catálogo', 'Pedidos', 'Contacto']

const funciones = [
  { titulo: 'Catálogo', texto: 'Mira todos los cafés disponibles y sus precios.', color: 'verde' },
  { titulo: 'Carrito', texto: 'Revisa lo que elegiste antes de comprar.', color: 'naranja' },
  { titulo: 'Mis pedidos', texto: 'Consulta el estado de tus compras.', color: 'lila' },
]

function App() {
  return (
    <div className="app">
      <nav className="nav">
        <div className="logo">El Cafetal</div>
        <ul className="nav-links">
          {enlaces.map((enlace) => (
            <li key={enlace}>
              <a href="#">{enlace}</a>
            </li>
          ))}
        </ul>
        <button className="btn btn-verde">Iniciar sesión</button>
      </nav>

      <header className="hero">
        <h1>Bienvenido a la tienda El Cafetal</h1>
        <p>Elige tu café, arma tu pedido y recíbelo sin complicaciones.</p>
        <button className="btn btn-oscuro">Ver catálogo</button>
      </header>

      <section className="tarjetas">
        {funciones.map((f) => (
          <article className="tarjeta" key={f.titulo}>
            <div className={`icono ${f.color}`} aria-hidden="true"></div>
            <h2>{f.titulo}</h2>
            <p>{f.texto}</p>
          </article>
        ))}
      </section>
    </div>
  )
}

export default App
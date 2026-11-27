import { useEffect, useMemo, useState } from "react";
import "./Ventas.css";

/* ============ AJUSTA ESTO A TU BACKEND ============ */
const API = "http://127.0.0.1:8000/api";
const RUTA_PRODUCTOS = "/productos/";
const RUTA_VENTAS = "/ventas/";
const RUTA_DETALLES = "/detalles/";
const TIPOS_PAGO = [
  { valor: "EFECTIVO", texto: "Efectivo" },
  { valor: "TRANSFERENCIA", texto: "Transferencia" },
  { valor: "TARJETA", texto: "Tarjeta" },
];
/* Campos que se leen de Producto: id, nombre, precio */
/* Campos que se envían a Venta: cliente, metodo_pago */
/* Campos que se envían a DetalleVenta: venta, producto, cantidad, precio_unitario */
/* ================================================== */

const dinero = (n) =>
  Number(n).toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

export default function Ventas() {
  const [productos, setProductos] = useState([]);
  const [cantidades, setCantidades] = useState({}); // { idProducto: cantidad a agregar }
  const [carrito, setCarrito] = useState([]); // [{ id, nombre, precio, cantidad }]
  const [abierta, setAbierta] = useState(false);
  const [form, setForm] = useState({ cliente: "", tipo_pago: "" });
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState("");
  const [aviso, setAviso] = useState("");

  useEffect(() => {
    fetch(API + RUTA_PRODUCTOS)
      .then((r) => r.json())
      .then((d) => setProductos(Array.isArray(d) ? d : d.results ?? []))
      .catch(() => setAviso("No se pudieron cargar los productos."));
  }, []);

  /* Cerrar la ventana con Escape */
  useEffect(() => {
    if (!abierta) return;
    const alTeclear = (e) => e.key === "Escape" && !enviando && cerrar();
    window.addEventListener("keydown", alTeclear);
    return () => window.removeEventListener("keydown", alTeclear);
  }, [abierta, enviando]);

  const total = useMemo(
    () => carrito.reduce((s, i) => s + i.precio * i.cantidad, 0),
    [carrito]
  );

  const cantidadDe = (id) => cantidades[id] ?? "1";

  const cambiarCantidad = (id, valor) =>
    setCantidades((c) => ({ ...c, [id]: valor }));

  const normalizarCantidad = (id) =>
    setCantidades((c) => ({
      ...c,
      [id]: String(Math.max(1, parseInt(c[id], 10) || 1)),
    }));

  const agregar = (p) => {
    const cantidad = Math.max(1, parseInt(cantidadDe(p.id), 10) || 1);
    setAviso("");
    setCarrito((actual) => {
      const existe = actual.find((i) => i.id === p.id);
      if (existe) {
        return actual.map((i) =>
          i.id === p.id ? { ...i, cantidad: i.cantidad + cantidad } : i
        );
      }
      return [...actual, { id: p.id, nombre: p.nombre, precio: Number(p.precio), cantidad }];
    });
    setCantidades((c) => ({ ...c, [p.id]: "1" }));
  };

  const quitar = (id) => setCarrito((c) => c.filter((i) => i.id !== id));

  const abrir = () => {
    if (carrito.length === 0) return;
    setError("");
    setAbierta(true);
  };

  const cerrar = () => {
    setAbierta(false);
    setError("");
  };

  const formCompleto =
    carrito.length > 0 && form.cliente.trim() && form.tipo_pago;

  const confirmarPago = async () => {
    if (carrito.length === 0) {
      setError("Agrega al menos un producto para poder comprar.");
      return;
    }
    setEnviando(true);
    setError("");
    try {
      // 1) crear la venta
      const rv = await fetch(API + RUTA_VENTAS, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cliente: form.cliente.trim(),
          metodo_pago: form.tipo_pago,
        }),
      });
      if (!rv.ok) {
        const detalle = await rv.text();
        throw new Error(`No se pudo crear la venta: ${detalle}`);
      }
      const venta = await rv.json();

      // 2) crear un detalle por cada producto del carrito
      for (const item of carrito) {
        const rd = await fetch(API + RUTA_DETALLES, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            venta: venta.id,
            producto: item.id,
            cantidad: item.cantidad,
            precio_unitario: item.precio,
          }),
        });
        if (!rd.ok) {
          const msg = await rd.text();
          throw new Error(`Falló "${item.nombre}": ${msg}`);
        }
      }

      // 3) todo salió bien: cerrar ventana y limpiar
      setCarrito([]);
      setForm({ cliente: "", tipo_pago: "" });
      setAbierta(false);
      setAviso("Pago confirmado. La venta quedó registrada.");
    } catch (e) {
      setError(e.message);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <section className="ventas">
      <h2 className="ventas__titulo">Ventas</h2>
      {aviso && <p className="ventas__aviso">{aviso}</p>}

      <div className="ventas__layout">
        {/* ============ IZQUIERDA: productos ============ */}
        <div className="ventas__productos">
          <h3>Productos</h3>
          {productos.length === 0 && <p className="vacio">No hay productos para mostrar.</p>}
          <ul className="lista">
            {productos.map((p) => (
              <li key={p.id} className="producto">
                <div className="producto__info">
                  <strong>{p.nombre}</strong>
                  <span>{dinero(p.precio)}</span>
                </div>
                <input
                  className="producto__cantidad"
                  type="number"
                  min="1"
                  value={cantidadDe(p.id)}
                  onChange={(e) => cambiarCantidad(p.id, e.target.value)}
                  onBlur={() => normalizarCantidad(p.id)}
                  aria-label={`Cantidad de ${p.nombre}`}
                />
                <button className="btn btn--agregar" onClick={() => agregar(p)}>
                  Agregar
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* ============ DERECHA: selección ============ */}
        <aside className="ventas__carrito">
          <h3>Tu selección</h3>
          {carrito.length === 0 ? (
            <p className="vacio">Agrega productos desde la lista de la izquierda.</p>
          ) : (
            <ul className="lista">
              {carrito.map((i) => (
                <li key={i.id} className="item">
                  <div className="item__info">
                    <strong>{i.nombre}</strong>
                    <span>
                      {i.cantidad} × {dinero(i.precio)}
                    </span>
                  </div>
                  <span className="item__subtotal">{dinero(i.precio * i.cantidad)}</span>
                  <button
                    className="btn btn--quitar"
                    onClick={() => quitar(i.id)}
                    aria-label={`Quitar ${i.nombre}`}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          )}

          <div className="carrito__total">
            <span>Total</span>
            <strong>{dinero(total)}</strong>
          </div>
          <button className="btn btn--comprar" onClick={abrir} disabled={carrito.length === 0}>
            Comprar
          </button>
        </aside>
      </div>

      {/* ============ VENTANA DE PAGO ============ */}
      {abierta && (
        <div className="modal" onClick={() => !enviando && cerrar()}>
          <div
            className="modal__caja"
            role="dialog"
            aria-modal="true"
            aria-labelledby="titulo-pago"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 id="titulo-pago">Datos de la compra</h3>

            <label>
              Nombre
              <input
                type="text"
                value={form.cliente}
                onChange={(e) => setForm({ ...form, cliente: e.target.value })}
                autoFocus
              />
            </label>

            <label>
              Tipo de pago
              <select
                value={form.tipo_pago}
                onChange={(e) => setForm({ ...form, tipo_pago: e.target.value })}
              >
                <option value="">Selecciona uno</option>
                {TIPOS_PAGO.map((t) => (
                  <option key={t.valor} value={t.valor}>
                    {t.texto}
                  </option>
                ))}
              </select>
            </label>


            <p className="modal__total">
              Total a pagar: <strong>{dinero(total)}</strong>
            </p>

            {error && <p className="modal__error">{error}</p>}

            <div className="modal__acciones">
              <button className="btn btn--cancelar" onClick={cerrar} disabled={enviando}>
                Cancelar
              </button>
              <button
                className="btn btn--confirmar"
                onClick={confirmarPago}
                disabled={!formCompleto || enviando}
              >
                {enviando ? "Procesando…" : "Confirmar pago"}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
import { Fragment, useEffect, useMemo, useState } from "react";
import "./Historial.css";

/* ============ AJUSTA ESTO A TU BACKEND ============ */
const API = "http://127.0.0.1:8000/api";
const RUTA_VENTAS = "/ventas/";
const RUTA_DETALLES = "/detalles/";
const RUTA_PRODUCTOS = "/productos/";
const METODOS = {
  EFECTIVO: "Efectivo",
  TRANSFERENCIA: "Transferencia",
  TARJETA: "Tarjeta",
};
/* Campos que se leen de Venta: id, fecha, cliente, metodo_pago */
/* Campos que se leen de DetalleVenta: venta, producto, cantidad, precio_unitario */
/* Campos que se leen de Producto: id, nombre */
/* ================================================== */

const dinero = (n) =>
  Number(n).toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

const fechaLegible = (iso) =>
  new Date(iso).toLocaleString("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  });

const comoLista = (d) => (Array.isArray(d) ? d : d.results ?? []);

export default function Historial() {
  const [ventas, setVentas] = useState([]);
  const [detalles, setDetalles] = useState([]);
  const [productos, setProductos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [abierta, setAbierta] = useState(null);

  const cargar = async () => {
    setCargando(true);
    setError("");
    try {
      const [rv, rd, rp] = await Promise.all([
        fetch(API + RUTA_VENTAS),
        fetch(API + RUTA_DETALLES),
        fetch(API + RUTA_PRODUCTOS),
      ]);
      if (!rv.ok || !rd.ok || !rp.ok) throw new Error("El servidor respondió con error.");
      setVentas(comoLista(await rv.json()));
      setDetalles(comoLista(await rd.json()));
      setProductos(comoLista(await rp.json()));
    } catch (e) {
      setError(`No se pudo cargar el historial. ${e.message}`);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargar();
  }, []);

  const nombreProducto = useMemo(() => {
    const mapa = {};
    productos.forEach((p) => (mapa[p.id] = p.nombre));
    return mapa;
  }, [productos]);

  const detallesPorVenta = useMemo(() => {
    const mapa = {};
    detalles.forEach((d) => {
      (mapa[d.venta] ??= []).push(d);
    });
    return mapa;
  }, [detalles]);

  const totalDe = (idVenta) =>
    (detallesPorVenta[idVenta] ?? []).reduce(
      (suma, d) => suma + (Number(d.cantidad) || 0) * (Number(d.precio_unitario) || 0),
      0
    );

  const visibles = ventas.filter((v) =>
    v.cliente.toLowerCase().includes(busqueda.trim().toLowerCase())
  );

  return (
    <section className="historial">
      <div className="historial__cabeza">
        <h2 className="historial__titulo">Historial de ventas</h2>
        <button className="hbtn" onClick={cargar} disabled={cargando}>
          {cargando ? "Cargando…" : "Actualizar"}
        </button>
      </div>

      <input
        className="historial__buscar"
        type="search"
        placeholder="Buscar por nombre del cliente"
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        aria-label="Buscar por nombre del cliente"
      />

      {error && <p className="historial__error">{error}</p>}

      {!error && !cargando && visibles.length === 0 && (
        <p className="historial__vacio">
          {ventas.length === 0
            ? "Todavía no hay ventas registradas."
            : "Ninguna venta coincide con tu búsqueda."}
        </p>
      )}

      {visibles.length > 0 && (
        <div className="historial__tabla-caja">
          <table className="historial__tabla">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Cliente</th>
                <th>Pago</th>
                <th className="num">Total</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {visibles.map((v) => {
                const items = detallesPorVenta[v.id] ?? [];
                const estaAbierta = abierta === v.id;
                return (
                  <Fragment key={v.id}>
                    <tr>
                      <td>{fechaLegible(v.fecha)}</td>
                      <td>{v.cliente}</td>
                      <td>{METODOS[v.metodo_pago] ?? v.metodo_pago}</td>
                      <td className="num">{dinero(totalDe(v.id))}</td>
                      <td className="acciones">
                        <button
                          className="hbtn"
                          onClick={() => setAbierta(estaAbierta ? null : v.id)}
                          aria-expanded={estaAbierta}
                        >
                          {estaAbierta ? "Ocultar" : "Ver detalle"}
                        </button>
                      </td>
                    </tr>
                    {estaAbierta && (
                      <tr className="detalle-fila">
                        <td colSpan={5}>
                          {items.length === 0 ? (
                            <p className="historial__vacio">Esta venta no tiene productos.</p>
                          ) : (
                            <ul className="detalle-lista">
                              {items.map((d) => (
                                <li key={d.id}>
                                  <span>
                                    {nombreProducto[d.producto] ?? `Producto ${d.producto}`}
                                  </span>
                                  <span>
                                    {d.cantidad} × {dinero(d.precio_unitario)}
                                  </span>
                                  <strong>
                                    {dinero(Number(d.cantidad) * Number(d.precio_unitario))}
                                  </strong>
                                </li>
                              ))}
                            </ul>
                          )}
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
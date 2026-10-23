from dominio.entidades import Producto
from dominio.puertos import ProductoRepositorioPort

from ..persistencia.db import get_connection


class SQLiteProductoRepositorio(ProductoRepositorioPort):
    def obtener_por_sku(self, sku: str) -> Producto | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM productos WHERE sku = ?", (sku,)
            ).fetchone()
            if row is None:
                return None
            return Producto(row["sku"], row["nombre"], row["stock"], row["precio"])

    def guardar(self, producto: Producto) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO productos VALUES (?, ?, ?, ?)",
                (producto.sku, producto.nombre, producto.stock, producto.precio),
            )

    def listar_todos(self) -> list[Producto]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM productos").fetchall()
            return [
                Producto(r["sku"], r["nombre"], r["stock"], r["precio"]) for r in rows
            ]

    def actualizar_stock(self, sku: str, nuevo_stock: int) -> None:
        with get_connection() as conn:
            conn.execute(
                "UPDATE productos SET stock = ? WHERE sku = ?", (nuevo_stock, sku)
            )

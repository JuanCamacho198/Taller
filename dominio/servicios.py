from .puertos import ProductoRepositorioPort


class ServicioVerificarDisponibilidad:
    def __init__(self, repo: ProductoRepositorioPort):
        self.repo = repo

    def ejecutar(self, sku: str) -> bool:
        producto = self.repo.obtener_por_sku(sku)
        return producto is not None and producto.stock > 0


class ServicioRegistrarMovimiento:
    def __init__(self, repo: ProductoRepositorioPort):
        self.repo = repo

    def ejecutar(self, sku: str, cantidad: int) -> None:
        producto = self.repo.obtener_por_sku(sku)
        if producto is None:
            raise ValueError(f"Producto {sku} no existe")
        nuevo_stock = producto.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("Stock insuficiente")
        self.repo.actualizar_stock(sku, nuevo_stock)


class ServicioObtenerResumen:
    def __init__(self, repo: ProductoRepositorioPort):
        self.repo = repo

    def ejecutar(self) -> list[dict]:
        productos = self.repo.listar_todos()
        return [
            {
                "sku": p.sku,
                "nombre": p.nombre,
                "stock": p.stock,
                "precio": p.precio,
                "stock_bajo": p.stock < 5,
            }
            for p in productos
        ]

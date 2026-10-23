from ..entidades import Producto
from ..puertos import ProductoRepositorioPort


class ServicioAgregarProducto:
    def __init__(self, repo: ProductoRepositorioPort):
        self.repo = repo

    def ejecutar(self, producto: Producto) -> None:
        if not producto.sku.strip() or not producto.nombre.strip():
            raise ValueError("SKU y nombre son obligatorios")
        if producto.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if producto.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.repo.obtener_por_sku(producto.sku) is not None:
            raise ValueError(f"El producto {producto.sku} ya existe")
        self.repo.guardar(producto)


class ServicioObtenerProducto:
    def __init__(self, repo: ProductoRepositorioPort):
        self.repo = repo

    def ejecutar(self, sku: str) -> Producto:
        producto = self.repo.obtener_por_sku(sku)
        if producto is None:
            raise ValueError(f"Producto {sku} no existe")
        return producto


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
                "sku": producto.sku,
                "nombre": producto.nombre,
                "stock": producto.stock,
                "precio": producto.precio,
                "stock_bajo": producto.stock < 5,
            }
            for producto in productos
        ]

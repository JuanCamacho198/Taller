from abc import ABC, abstractmethod
from .entidades import Producto


class ProductoRepositorioPort(ABC):
    @abstractmethod
    def obtener_por_sku(self, sku: str) -> Producto | None:
        pass

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Producto]:
        pass

    @abstractmethod
    def actualizar_stock(self, sku: str, nuevo_stock: int) -> None:
        pass

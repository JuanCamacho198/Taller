from dataclasses import dataclass


@dataclass
class Producto:
    sku: str
    nombre: str
    stock: int
    precio: float
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from dominio.entidades import Producto
from dominio.servicios import (
    ServicioAgregarProducto,
    ServicioObtenerProducto,
    ServicioObtenerResumen,
    ServicioRegistrarMovimiento,
    ServicioVerificarDisponibilidad,
)

from ..repositorios import SQLiteProductoRepositorio

bp = Blueprint("inventario", __name__, url_prefix="/inventario")
repo = SQLiteProductoRepositorio()


@bp.get("/existe/<sku>")
def existe(sku: str):
    disponible: bool = ServicioVerificarDisponibilidad(repo).ejecutar(sku)
    return jsonify({"sku": sku, "disponible": disponible})


@bp.post("/movimiento")
def movimiento():
    data = request.get_json(force=True)
    ServicioRegistrarMovimiento(repo).ejecutar(data["sku"], int(data["cantidad"]))
    return "", 204


@bp.post("/productos")
def agregar_producto():
    data = request.get_json(force=True)
    producto = Producto(
        sku=data["sku"].strip(),
        nombre=data["nombre"].strip(),
        stock=int(data["stock"]),
        precio=float(data["precio"]),
    )
    ServicioAgregarProducto(repo).ejecutar(producto)
    return jsonify({"sku": producto.sku, "mensaje": "Producto agregado"}), 201


@bp.get("/productos/<sku>")
def obtener_producto(sku: str):
    producto = ServicioObtenerProducto(repo).ejecutar(sku)
    return jsonify(
        {
            "sku": producto.sku,
            "nombre": producto.nombre,
            "stock": producto.stock,
            "precio": producto.precio,
        }
    )


@bp.get("/resumen")
def resumen():
    resultado: list[dict] = ServicioObtenerResumen(repo).ejecutar()
    return jsonify(resultado)


@bp.get("/")
def vista():
    sku = request.args.get("sku_verificar", "")
    sku_producto = request.args.get("sku_producto", "")
    disponible = ServicioVerificarDisponibilidad(repo).ejecutar(sku) if sku else None
    producto_consultado = None
    error_producto = None
    if sku_producto:
        try:
            producto_consultado = ServicioObtenerProducto(repo).ejecutar(sku_producto)
        except ValueError as e:
            error_producto = str(e)
    return render_template(
        "index.html",
        resumen=ServicioObtenerResumen(repo).ejecutar(),
        sku_verificar=sku,
        disponible=disponible,
        sku_producto=sku_producto,
        producto_consultado=producto_consultado,
        error_producto=error_producto,
        mensaje=request.args.get("mensaje"),
        error=request.args.get("error"),
    )


@bp.post("/ui/movimiento")
def ui_movimiento():
    try:
        ServicioRegistrarMovimiento(repo).ejecutar(
            request.form["sku"], int(request.form["cantidad"])
        )
        return redirect(url_for("inventario.vista", mensaje="Movimiento guardado"))
    except (ValueError, KeyError) as e:
        return redirect(url_for("inventario.vista", mensaje=str(e), error="1"))


@bp.post("/ui/productos")
def ui_agregar_producto():
    try:
        producto = Producto(
            sku=request.form["sku"].strip(),
            nombre=request.form["nombre"].strip(),
            stock=int(request.form["stock"]),
            precio=float(request.form["precio"]),
        )
        ServicioAgregarProducto(repo).ejecutar(producto)
        return redirect(url_for("inventario.vista", mensaje="Producto agregado"))
    except (ValueError, KeyError) as e:
        return redirect(url_for("inventario.vista", mensaje=str(e), error="1"))

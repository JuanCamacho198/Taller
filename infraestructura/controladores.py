from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from dominio.servicios import (
    ServicioVerificarDisponibilidad,
    ServicioRegistrarMovimiento,
    ServicioObtenerResumen,
)
from .repositorios import SQLiteProductoRepositorio

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


@bp.get("/resumen")
def resumen():
    resultado: list[dict] = ServicioObtenerResumen(repo).ejecutar()
    return jsonify(resultado)


@bp.get("/")
def vista():
    sku = request.args.get("sku_verificar", "")
    disponible = ServicioVerificarDisponibilidad(repo).ejecutar(sku) if sku else None
    return render_template(
        "index.html",
        resumen=ServicioObtenerResumen(repo).ejecutar(),
        sku_verificar=sku,
        disponible=disponible,
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

from flask import Flask, redirect
from infraestructura.persistencia.db import init_db
from infraestructura.controladores import bp


def create_app() -> Flask:
    app = Flask(__name__)
    init_db()
    app.register_blueprint(bp)

    @app.get("/")
    def index():
        return redirect("/inventario/")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

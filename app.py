from flask import Flask, redirect
from infraestructura.persistencia.db import init_db
from infraestructura.controladores import bp


def create_app() -> Flask:
    application = Flask(__name__)
    init_db()
    application.register_blueprint(bp)

    @application.get("/")
    def index():
        return redirect("/inventario/")

    return application


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

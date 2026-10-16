import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "inventario.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                sku TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                stock INTEGER NOT NULL,
                precio REAL NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO productos VALUES ('SKU001', 'Tornillo', 10, 0.5)"
        )
        conn.execute(
            "INSERT OR IGNORE INTO productos VALUES ('SKU002', 'Tuerca', 2, 0.3)"
        )

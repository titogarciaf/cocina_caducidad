# db.py
import sqlite3
from pathlib import Path
from kivy.utils import platform

def _android_db_path():
    # almacén interno de la app (no requiere permisos extra)
    try:
        from android.storage import app_storage_path
        base = Path(app_storage_path())
        base.mkdir(parents=True, exist_ok=True)
        return base / "caducidad.db"
    except Exception:
        # fallback
        return Path(__file__).parent / "caducidad.db"

if platform == "android":
    DB_PATH = _android_db_path()
else:
    DB_PATH = Path(__file__).parent / "caducidad.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad TEXT,
        caduca DATE NOT NULL,
        categoria TEXT NOT NULL DEFAULT 'Otros'
    )
    """)
    try:
        conn.execute("ALTER TABLE items ADD COLUMN categoria TEXT DEFAULT 'Otros'")
    except sqlite3.OperationalError:
        pass
    return conn

def add_item(nombre, cantidad, caduca_iso, categoria):
    with get_conn() as c:
        c.execute(
            "INSERT INTO items(nombre,cantidad,caduca,categoria) VALUES(?,?,?,?)",
            (nombre, cantidad, caduca_iso, categoria)
        )

def update_item(item_id, nombre, cantidad, caduca_iso, categoria):
    with get_conn() as c:
        c.execute(
            "UPDATE items SET nombre=?, cantidad=?, caduca=?, categoria=? WHERE id=?",
            (nombre, cantidad, caduca_iso, categoria, item_id)
        )

def delete_item(item_id):
    with get_conn() as c:
        c.execute("DELETE FROM items WHERE id=?", (item_id,))

def list_items(category=None):
    with get_conn() as c:
        if category and category not in ("Todos", ""):
            cur = c.execute(
                "SELECT id, nombre, cantidad, caduca, categoria FROM items WHERE categoria=? ORDER BY date(caduca) ASC",
                (category,)
            )
        else:
            cur = c.execute("SELECT id, nombre, cantidad, caduca, categoria FROM items ORDER BY date(caduca) ASC")
        return cur.fetchall()

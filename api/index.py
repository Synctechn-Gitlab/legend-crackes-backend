import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import_log = []

def try_import(name, func):
    try:
        func()
        import_log.append(f"SUCCESS: {name}")
    except Exception as e:
        import traceback
        import_log.append(f"FAILED: {name} -> {type(e).__name__}: {e}\n{traceback.format_exc()}")

try_import("fastapi", lambda: __import__("fastapi"))
try_import("sqlalchemy", lambda: __import__("sqlalchemy"))
try_import("pg8000", lambda: __import__("pg8000"))
try_import("jwt", lambda: __import__("jwt"))
try_import("bcrypt", lambda: __import__("bcrypt"))
try_import("app.core.config", lambda: __import__("app.core.config", fromlist=["settings"]))
try_import("app.core.database", lambda: __import__("app.core.database", fromlist=["engine"]))
try_import("app.models", lambda: __import__("app.models"))
try_import("app.routers.categories", lambda: __import__("app.routers.categories"))
try_import("app.main", lambda: __import__("app.main", fromlist=["app"]))

from fastapi import FastAPI
app = FastAPI()

@app.get("/{path:path}")
def catch_all(path: str = ""):
    return {"status": "ok", "log": import_log}

__all__ = ["app"]

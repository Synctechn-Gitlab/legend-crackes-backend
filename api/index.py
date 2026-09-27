import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as raw_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")

        if path.startswith("/api/index.py"):
            new_path = path[13:]
            scope["path"] = new_path if new_path else "/"
            scope["raw_path"] = scope["path"].encode("utf-8")
        elif path.startswith("/api/index"):
            new_path = path[10:]
            scope["path"] = new_path if new_path else "/"
            scope["raw_path"] = scope["path"].encode("utf-8")

    await raw_app(scope, receive, send)

__all__ = ["app"]

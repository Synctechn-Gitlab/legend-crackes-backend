import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")
        # Strip Vercel function path prefixes if present
        for prefix in ["/api/index.py", "/api/index"]:
            if path == prefix or path.startswith(prefix + "/"):
                new_path = path[len(prefix):]
                scope["path"] = new_path if new_path else "/"
                break
    await fastapi_app(scope, receive, send)

__all__ = ["app"]

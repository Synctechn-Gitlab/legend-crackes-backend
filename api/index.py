import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as raw_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        headers = dict(scope.get("headers", []))
        
        # Check Vercel forwarded URI headers
        forwarded_uri = headers.get(b"x-forwarded-uri", b"").decode("utf-8").split("?")[0]
        matched_path = headers.get(b"x-matched-path", b"").decode("utf-8").split("?")[0]
        
        if forwarded_uri and not forwarded_uri.startswith("/api/index"):
            scope["path"] = forwarded_uri
        elif matched_path and not matched_path.startswith("/api/index"):
            scope["path"] = matched_path
        else:
            path = scope.get("path", "")
            for prefix in ["/api/index.py", "/api/index"]:
                if path == prefix or path.startswith(prefix + "/"):
                    new_path = path[len(prefix):]
                    scope["path"] = new_path if new_path else "/"
                    break

    await raw_app(scope, receive, send)

__all__ = ["app"]

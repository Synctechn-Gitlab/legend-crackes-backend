import os
import sys
import urllib.parse

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as raw_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        qs_bytes = scope.get("query_string", b"")
        qs_str = qs_bytes.decode("utf-8", errors="ignore")

        if "path=" in qs_str:
            parsed = urllib.parse.parse_qs(qs_str, keep_blank_values=True)
            path_list = parsed.pop("path", None)
            if path_list and path_list[0]:
                target_path = "/" + path_list[0].lstrip("/")
                scope["path"] = target_path
                scope["raw_path"] = target_path.encode("utf-8")
                scope["query_string"] = urllib.parse.urlencode(parsed, doseq=True).encode("utf-8")
        elif scope.get("path", "").startswith("/api/index"):
            scope["path"] = "/"
            scope["raw_path"] = b"/"

    await raw_app(scope, receive, send)

__all__ = ["app"]

import os
import sys
import json
import urllib.parse

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as raw_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        qs_bytes = scope.get("query_string", b"")
        qs_str = qs_bytes.decode("utf-8", errors="ignore")
        headers = dict(scope.get("headers", []))
        headers_dict = {k.decode("utf-8", errors="ignore"): v.decode("utf-8", errors="ignore") for k, v in headers.items()}

        # Immediate diagnostic response for debugging Vercel scope & query parameters
        if "debug=1" in qs_str or scope.get("path") == "/debug":
            body = json.dumps({
                "scope_path": scope.get("path"),
                "query_string": qs_str,
                "headers": headers_dict
            }, indent=2).encode("utf-8")

            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")]
            })
            await send({
                "type": "http.response.body",
                "body": body
            })
            return

        if "path=" in qs_str:
            parsed = urllib.parse.parse_qs(qs_str, keep_blank_values=True)
            path_list = parsed.pop("path", None)
            if path_list and path_list[0]:
                target_path = "/" + path_list[0].lstrip("/")
                scope["path"] = target_path
                scope["query_string"] = urllib.parse.urlencode(parsed, doseq=True).encode("utf-8")
        elif scope.get("path", "").startswith("/api/index"):
            scope["path"] = "/"

    await raw_app(scope, receive, send)

__all__ = ["app"]

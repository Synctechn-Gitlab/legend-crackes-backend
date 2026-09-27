import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

err_msg = ""
try:
    from app.main import app as _app
except Exception as e:
    _app = None
    err_msg = f"IMPORT FAILURE: {type(e).__name__}: {e}\n{traceback.format_exc()}"

async def app(scope, receive, send):
    if scope["type"] == "http":
        if err_msg or not _app:
            body = (err_msg or "No app loaded").encode("utf-8")
            await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": body})
            return
        await _app(scope, receive, send)

__all__ = ["app"]

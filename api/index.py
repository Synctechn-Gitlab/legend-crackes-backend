import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app as fastapi_app
    import_error = None
except Exception as e:
    fastapi_app = None
    import_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

async def app(scope, receive, send):
    if scope["type"] == "http":
        if import_error:
            body = f"IMPORT ERROR:\n{import_error}".encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"text/plain")]
            })
            await send({
                "type": "http.response.body",
                "body": body
            })
            return

        try:
            await fastapi_app(scope, receive, send)
        except Exception as e:
            err_str = f"RUNTIME ERROR:\n{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"text/plain")]
            })
            await send({
                "type": "http.response.body",
                "body": err_str.encode("utf-8")
            })

__all__ = ["app"]

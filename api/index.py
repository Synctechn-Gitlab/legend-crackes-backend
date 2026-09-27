from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all(request: Request, path: str = ""):
    log = []

    def try_mod(name, code):
        try:
            exec(code, globals())
            log.append(f"SUCCESS: {name}")
        except Exception as e:
            import traceback
            log.append(f"FAILED: {name} -> {type(e).__name__}: {e}\n{traceback.format_exc()}")

    try_mod("fastapi", "import fastapi")
    try_mod("sqlalchemy", "import sqlalchemy")
    try_mod("pg8000", "import pg8000")
    try_mod("psycopg2", "import psycopg2")
    try_mod("bcrypt", "import bcrypt")
    try_mod("jwt", "import jwt")
    try_mod("config", "from app.core.config import settings")
    try_mod("database", "from app.core.database import engine")
    try_mod("models", "import app.models")
    try_mod("main", "from app.main import app as main_app")

    return PlainTextResponse("\n========================================\n".join(log))

__all__ = ["app"]

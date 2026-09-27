import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} on http://localhost:{settings.APP_PORT}")
    print(f"Interactive Swagger Docs: http://localhost:{settings.APP_PORT}/docs")
    print(f"ReDoc Documentation:     http://localhost:{settings.APP_PORT}/redoc")
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=(settings.ENVIRONMENT == "development")
    )

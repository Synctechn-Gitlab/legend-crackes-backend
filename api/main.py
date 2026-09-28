from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sivakasi Fireworks Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "online", "message": "Backend API is running on Vercel"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/categories")
def get_categories():
    return [
        {"id": 1, "name": "Sparklers", "slug": "sparklers", "description": "Traditional Sivakasi Ground & Hand Sparklers", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819", "is_active": True, "product_count": 45},
        {"id": 2, "name": "Ground Chakkars", "slug": "ground-chakkars", "description": "Spinning Ground Wheels & Flower Pots", "image_url": "https://images.unsplash.com/photo-1531747056595-07f6cbbe10ad", "is_active": True, "product_count": 32},
        {"id": 3, "name": "Flower Pots", "slug": "flower-pots", "description": "Vibrant Fountain Crackers & Flower Pots", "image_url": "https://images.unsplash.com/photo-1498931299472-f7a63a5a1cfa", "is_active": True, "product_count": 28},
        {"id": 4, "name": "Rockets", "slug": "rockets", "description": "High Flying Sound & Light Rockets", "image_url": "https://images.unsplash.com/photo-1513151233558-d860c5398176", "is_active": True, "product_count": 30},
        {"id": 5, "name": "Single & Multi Sound Crackers", "slug": "sound-crackers", "description": "Classic Sivakasi Sound Crackers & Garlands", "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f", "is_active": True, "product_count": 50},
        {"id": 6, "name": "Fancy Aerial Shots", "slug": "aerial-shots", "description": "Multi-shot Sky Fountains & Color Displays", "image_url": "https://images.unsplash.com/photo-1498931299472-f7a63a5a1cfa", "is_active": True, "product_count": 40},
        {"id": 7, "name": "Kids Special", "slug": "kids-special", "description": "Safe Sparklers, Roll Caps & Pop-Pops", "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819", "is_active": True, "product_count": 25},
        {"id": 8, "name": "Gift Boxes", "slug": "gift-boxes", "description": "Assorted Festival Family Cracker Packs", "image_url": "https://images.unsplash.com/photo-1513151233558-d860c5398176", "is_active": True, "product_count": 15}
    ]

__all__ = ["app"]

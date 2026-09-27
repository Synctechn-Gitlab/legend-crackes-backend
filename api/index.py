import os
import sys

# Ensure root directory is in sys.path for relative and absolute imports in Vercel Serverless environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

__all__ = ["app"]

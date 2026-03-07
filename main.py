"""AI Visibility Score - FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.analysis_router import router as analysis_router

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    yield


app = FastAPI(
    title="AI Visibility Score API",
    description="Analyzes how visible a website is in ChatGPT recommendations",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(analysis_router, prefix="/analyse")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def index():
    """Serve the landing page."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/blog")
async def blog():
    """Serve the blog page."""
    return FileResponse(STATIC_DIR / "blog.html")


@app.get("/help")
async def docs():
    """Serve the documentation page."""
    return FileResponse(STATIC_DIR / "docs.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

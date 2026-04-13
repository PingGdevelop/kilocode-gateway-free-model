from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from typing import List, Dict, Any
import logging
import sys
import aiofiles
from contextlib import asynccontextmanager


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration constants
KILO_API_URL = "https://api.kilo.ai/api/gateway/models"
REQUEST_TIMEOUT = 10
CACHE_TTL = 60  # Cache responses for 60 seconds

# Global cached state
_cached_models = None
_cache_timestamp = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize shared HTTP client on startup
    app.state.http_client = httpx.AsyncClient(timeout=REQUEST_TIMEOUT)
    logger.info("Application started, HTTP client initialized")

    yield

    # Cleanup on shutdown
    await app.state.http_client.aclose()
    logger.info("Application shutdown, HTTP client closed")


app = FastAPI(
    title="Kilo Gateway API",
    lifespan=lifespan,
    description="Gateway proxy for Kilo.ai free models"
)

# CORS Configuration - Restricted for production safety
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
    max_age=86400,
)

app.mount("/static", StaticFiles(directory="static", check_dir=True), name="static")


async def fetch_kilo_models() -> Dict[str, Any]:
    """Fetch and cache models from Kilo API with TTL"""
    global _cached_models, _cache_timestamp
    import time

    now = time.time()

    # Return cached data if still valid
    if _cached_models is not None and now - _cache_timestamp < CACHE_TTL:
        logger.debug("Returning cached models data")
        return _cached_models

    logger.info("Fetching fresh models from Kilo API")

    try:
        response = await app.state.http_client.get(KILO_API_URL)
        response.raise_for_status()
        data = response.json()

        # Update cache
        _cached_models = data
        _cache_timestamp = now

        return data
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch models from Kilo API: {str(e)}")
        raise HTTPException(status_code=503, detail="Upstream API unavailable")
    except Exception as e:
        logger.error(f"Unexpected error fetching models: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/", response_class=HTMLResponse)
async def root():
    async with aiofiles.open("static/index.html", mode="r") as f:
        content = await f.read()
    return HTMLResponse(content=content)


@app.get("/api/models", summary="Get all available models")
async def get_all_models():
    return await fetch_kilo_models()


def is_free_model(model: Dict[str, Any]) -> bool:
    """Check if a model is free based on pricing or name/ID."""
    pricing = model.get("pricing", {})
    prompt_price = str(pricing.get("prompt", ""))
    completion_price = str(pricing.get("completion", ""))
    model_id = model.get("id", "")
    model_name = model.get("name", "").lower()

    # Free if: price is "0", or ":free" in ID, or "free" in name
    return (
        (prompt_price == "0" and completion_price == "0") or
        ":free" in model_id or
        "free" in model_name
    )


@app.get("/api/models/free", summary="Get only free models")
async def get_free_models():
    data = await fetch_kilo_models()

    free_models = []
    for model in data.get("data", []):
        if is_free_model(model):
            free_models.append({
                "id": model.get("id"),
                "name": model.get("name"),
                "description": model.get("description"),
                "context_length": model.get("context_length"),
                "architecture": model.get("architecture"),
                "supported_parameters": model.get("supported_parameters"),
            })

    logger.info(f"Returned {len(free_models)} free models")
    return {"data": free_models}


@app.get("/health", summary="Service health check")
async def health_check():
    return {"status": "ok", "service": "kilo-gateway-free-model"}


if __name__ == "__main__":
    import uvicorn

    # Get port from command line arguments
    port = 8000
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])

    logger.info(f"Starting server at http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

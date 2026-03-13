from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from typing import List, Dict, Any

app = FastAPI(title="Kilo Gateway API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

KILO_API_URL = "https://api.kilo.ai/api/gateway/models"


@app.get("/")
async def root():
    return HTMLResponse(open("static/index.html").read())


@app.get("/api/models")
async def get_all_models():
    async with httpx.AsyncClient() as client:
        response = await client.get(KILO_API_URL)
        response.raise_for_status()
        return response.json()


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


@app.get("/api/models/free")
async def get_free_models():
    async with httpx.AsyncClient() as client:
        response = await client.get(KILO_API_URL)
        response.raise_for_status()
        data = response.json()
        
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
    
    return {"data": free_models}


if __name__ == "__main__":
    import uvicorn
    print("Starting server at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

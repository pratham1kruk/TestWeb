from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import httpx
import os

load_dotenv()  # Load RAWG_API_KEY and GIANTBOMB_API_KEY from .env

from models import (
    GameLoraResponse, FranchiseTimeline, StudioHistory,
    GameSearchResult, SuccessorPredecessorMap
)
from services.rawg import RAWGService
from services.giantbomb import GiantBombService
from services.aggregator import GameAggregator


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=15.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="🎮 Game Lore Encyclopedia API",
    description="""
A comprehensive game metadata API aggregating data from **RAWG** and **GiantBomb**.

## Endpoints

| # | Endpoint | Description |
|---|----------|-------------|
| 🕹 | `GET /search?name=<game>` | Full game details — release, studio, story |
| 📖 | `GET /lore/{slug}` | Description, storyline, themes, lore |
| 🏗 | `GET /franchise/{name}/timeline` | All franchise entries in chronological order |
| 🏢 | `GET /studio/{name}/games` | All games from a developer in release order |
| 🔀 | `GET /series/{game}/chain` | Predecessor → Successor chain |

## Data Sources
- [RAWG](https://rawg.io/apidocs) — Game metadata, ratings, screenshots, series
- [GiantBomb](https://www.giantbomb.com/api/) — Lore, storylines, themes, franchises
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_aggregator(request: Request) -> GameAggregator:
    client = request.app.state.http_client
    rawg_key = os.getenv("RAWG_API_KEY", "")
    gb_key = os.getenv("GIANTBOMB_API_KEY", "")
    return GameAggregator(RAWGService(client, rawg_key), GiantBombService(client, gb_key))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb = traceback.format_exc()
    print(f"\n[ERROR] {request.method} {request.url}\n{tb}")
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=500, content={"detail": str(exc), "traceback": tb})


@app.get("/", tags=["Health"], summary="API root & health check")
async def root():
    return {
        "api": "Game Lore Encyclopedia",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "search": "/search?name=<game_name>",
            "lore": "/lore/<game_slug>",
            "franchise_timeline": "/franchise/<franchise_name>/timeline",
            "studio_history": "/studio/<studio_name>/games",
            "series_chain": "/series/<game_name>/chain",
        },
        "docs": "/docs",
    }


@app.get(
    "/search",
    response_model=GameSearchResult,
    tags=["Core"],
    summary="🕹 Search game by name — full details",
    description="Search by game title. Returns release info, studio, story, ratings, themes, series.",
)
async def search_game(
    request: Request,
    name: str = Query(..., description="Game title to search", example="The Witcher 3"),
):
    agg = _get_aggregator(request)
    result = await agg.search_game(name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Game '{name}' not found.")
    return result


@app.get(
    "/lore/{game_slug}",
    response_model=GameLoraResponse,
    tags=["Lore"],
    summary="📖 Get lore, storyline, themes for a game",
    description="Pass the RAWG slug (e.g. `the-witcher-3-wild-hunt`) to get full lore, themes, and storyline.",
)
async def get_game_lore(request: Request, game_slug: str):
    agg = _get_aggregator(request)
    result = await agg.get_lore(game_slug)
    if not result:
        raise HTTPException(status_code=404, detail=f"Lore for '{game_slug}' not found.")
    return result


@app.get(
    "/franchise/{franchise_name}/timeline",
    response_model=FranchiseTimeline,
    tags=["Franchise"],
    summary="🏗 Franchise timeline — all entries in order",
    description="Get every game in a franchise sorted by release date.",
)
async def get_franchise_timeline(request: Request, franchise_name: str):
    agg = _get_aggregator(request)
    result = await agg.get_franchise_timeline(franchise_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Franchise '{franchise_name}' not found.")
    return result


@app.get(
    "/studio/{studio_name}/games",
    response_model=StudioHistory,
    tags=["Studio"],
    summary="🏢 All games from a studio in release order",
    description="List all games developed by a studio in chronological order.",
)
async def get_studio_history(request: Request, studio_name: str):
    agg = _get_aggregator(request)
    result = await agg.get_studio_history(studio_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Studio '{studio_name}' not found.")
    return result


@app.get(
    "/series/{game_name}/chain",
    response_model=SuccessorPredecessorMap,
    tags=["Series"],
    summary="🔀 Successor-Predecessor chain for a game series",
    description="Enter any game in a series to get the full ordered chain with predecessor/successor links.",
)
async def get_series_chain(request: Request, game_name: str):
    agg = _get_aggregator(request)
    result = await agg.get_series_chain(game_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Series chain for '{game_name}' not found.")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5001, reload=True)

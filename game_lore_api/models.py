from pydantic import BaseModel, Field
from typing import Optional, List


class Platform(BaseModel):
    name: str
    slug: Optional[str] = None


class Genre(BaseModel):
    name: str
    slug: Optional[str] = None


class Screenshot(BaseModel):
    url: str


class Developer(BaseModel):
    name: str
    slug: Optional[str] = None


class Publisher(BaseModel):
    name: str
    slug: Optional[str] = None


class Rating(BaseModel):
    source: str
    score: Optional[float] = None
    max_score: Optional[float] = None


# ─────────────────────────────────────────────
# 1. GAME LORE RESPONSE
# ─────────────────────────────────────────────
class GameLoraResponse(BaseModel):
    slug: str
    name: str
    description: Optional[str] = Field(None, description="Full game description")
    storyline: Optional[str] = Field(None, description="Main storyline summary")
    themes: List[str] = Field(default_factory=list, description="Narrative/gameplay themes")
    lore_summary: Optional[str] = Field(None, description="Lore aggregated from GiantBomb/RAWG")
    genres: List[Genre] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    cover_image: Optional[str] = None
    screenshots: List[Screenshot] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list, description="Data sources used")


# ─────────────────────────────────────────────
# 2. FRANCHISE TIMELINE
# ─────────────────────────────────────────────
class FranchiseEntry(BaseModel):
    position: int
    name: str
    slug: Optional[str] = None
    release_date: Optional[str] = None
    release_year: Optional[int] = None
    entry_type: Optional[str] = Field(None, description="main, prequel, sequel, remake, spin-off")
    platforms: List[str] = Field(default_factory=list)
    cover_image: Optional[str] = None
    rating: Optional[float] = None
    short_description: Optional[str] = None


class FranchiseTimeline(BaseModel):
    franchise_name: str
    total_entries: int
    entries: List[FranchiseEntry] = Field(description="Sorted chronologically by release date")
    sources: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# 3. STUDIO HISTORY
# ─────────────────────────────────────────────
class StudioGame(BaseModel):
    position: int
    name: str
    slug: Optional[str] = None
    release_date: Optional[str] = None
    release_year: Optional[int] = None
    genres: List[str] = Field(default_factory=list)
    platforms: List[str] = Field(default_factory=list)
    rating: Optional[float] = None
    cover_image: Optional[str] = None


class StudioHistory(BaseModel):
    studio_name: str
    slug: Optional[str] = None
    country: Optional[str] = None
    founded: Optional[str] = None
    description: Optional[str] = None
    total_games: int
    games: List[StudioGame] = Field(description="Sorted by release date ascending")
    sources: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# 4. GAME SEARCH RESULT
# ─────────────────────────────────────────────
class GameSearchResult(BaseModel):
    name: str
    slug: Optional[str] = None
    release_date: Optional[str] = None
    release_year: Optional[int] = None
    developers: List[Developer] = Field(default_factory=list)
    publishers: List[Publisher] = Field(default_factory=list)
    platforms: List[Platform] = Field(default_factory=list)
    genres: List[Genre] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    storyline: Optional[str] = None
    lore_summary: Optional[str] = None
    cover_image: Optional[str] = None
    screenshots: List[Screenshot] = Field(default_factory=list)
    ratings: List[Rating] = Field(default_factory=list)
    metacritic: Optional[int] = None
    franchise: Optional[str] = None
    series: Optional[str] = None
    website: Optional[str] = None
    sources: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# 5. SUCCESSOR-PREDECESSOR MAP
# ─────────────────────────────────────────────
class SeriesNode(BaseModel):
    position: int
    name: str
    slug: Optional[str] = None
    release_year: Optional[int] = None
    release_date: Optional[str] = None
    relation: str = Field(description="main, prequel, sequel, remake, spin-off, remaster")
    predecessor: Optional[str] = Field(None, description="Name of the previous game in chain")
    successor: Optional[str] = Field(None, description="Name of the next game in chain")
    cover_image: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    short_description: Optional[str] = None


class SuccessorPredecessorMap(BaseModel):
    query_game: str
    series_name: Optional[str] = None
    total_entries: int
    chain: List[SeriesNode] = Field(description="Full ordered chain from first to latest")
    sources: List[str] = Field(default_factory=list)

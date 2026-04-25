import asyncio
import re
from typing import Optional, List, Dict, Any

from services.rawg import RAWGService
from services.giantbomb import GiantBombService
from models import (
    GameLoraResponse, FranchiseTimeline, FranchiseEntry,
    StudioHistory, StudioGame, GameSearchResult, GameSearchResult,
    SuccessorPredecessorMap, SeriesNode,
    Platform, Genre, Developer, Publisher, Rating, Screenshot
)


def _strip_html(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean or None


def _parse_year(date_str: Optional[str]) -> Optional[int]:
    if not date_str:
        return None
    try:
        return int(date_str[:4])
    except (ValueError, TypeError):
        return None


def _cover(rawg_game: Optional[Dict]) -> Optional[str]:
    if not rawg_game:
        return None
    return rawg_game.get("background_image")


def _platforms_from_rawg(rawg_game: Dict) -> List[str]:
    plats = rawg_game.get("platforms") or []
    return [p["platform"]["name"] for p in plats if p.get("platform", {}).get("name")]


def _genres_from_rawg(rawg_game: Dict) -> List[Genre]:
    return [Genre(name=g["name"], slug=g.get("slug")) for g in rawg_game.get("genres") or []]


def _tags_from_rawg(rawg_game: Dict) -> List[str]:
    return [t["name"] for t in (rawg_game.get("tags") or [])[:15]]


def _determine_relation(game: Dict, query_name: str) -> str:
    name = game.get("name", "").lower()
    if "remaster" in name or "hd" in name:
        return "remaster"
    if "remake" in name:
        return "remake"
    if "prequel" in name or "origins" in name or "zero" in name:
        return "prequel"
    if "episode" in name or "chapter" in name:
        return "episode"
    return "main"


class GameAggregator:
    def __init__(self, rawg: RAWGService, gb: GiantBombService):
        self.rawg = rawg
        self.gb = gb

    # ─────────────────────────────────────────────
    # 1. SEARCH GAME — full details
    # ─────────────────────────────────────────────
    async def search_game(self, name: str) -> Optional[GameSearchResult]:
        rawg_game, gb_game = await asyncio.gather(
            self.rawg.search_game(name),
            self.gb.search_game(name),
        )
        if not rawg_game:
            return None

        slug = rawg_game.get("slug", "")

        # Get full details from RAWG (basic search is shallow)
        rawg_detail, screenshots = await asyncio.gather(
            self.rawg.get_game_details(slug),
            self.rawg.get_game_screenshots(slug),
        )
        rawg_full = rawg_detail or rawg_game

        # GiantBomb lore enrichment
        gb_lore = self.gb.extract_lore(gb_game) if gb_game else {}
        themes = gb_lore.get("themes") or []
        franchise = (gb_lore.get("franchises") or [None])[0]

        # Parse developers / publishers
        devs = [Developer(name=d["name"], slug=d.get("slug")) for d in (rawg_full.get("developers") or [])]
        pubs = [Publisher(name=p["name"], slug=p.get("slug")) for p in (rawg_full.get("publishers") or [])]

        sources = ["RAWG"]
        if gb_game:
            sources.append("GiantBomb")

        release_date = rawg_full.get("released")

        return GameSearchResult(
            name=rawg_full.get("name", ""),
            slug=slug,
            release_date=release_date,
            release_year=_parse_year(release_date),
            developers=devs,
            publishers=pubs,
            platforms=[Platform(name=p) for p in _platforms_from_rawg(rawg_full)],
            genres=_genres_from_rawg(rawg_full),
            themes=themes,
            tags=_tags_from_rawg(rawg_full),
            description=_strip_html(rawg_full.get("description") or rawg_full.get("description_raw")),
            storyline=_strip_html(rawg_full.get("description_raw")),
            lore_summary=_strip_html(gb_lore.get("deck") or gb_lore.get("description")),
            cover_image=_cover(rawg_full) or gb_lore.get("image"),
            screenshots=[Screenshot(url=s["image"]) for s in screenshots if s.get("image")],
            ratings=[
                Rating(source="Metacritic", score=rawg_full.get("metacritic"), max_score=100),
                Rating(source="RAWG", score=rawg_full.get("rating"), max_score=rawg_full.get("rating_top")),
            ],
            metacritic=rawg_full.get("metacritic"),
            franchise=franchise,
            website=rawg_full.get("website"),
            sources=sources,
        )

    # ─────────────────────────────────────────────
    # 2. GAME LORE
    # ─────────────────────────────────────────────
    async def get_lore(self, game_slug: str) -> Optional[GameLoraResponse]:
        rawg_detail, gb_game = await asyncio.gather(
            self.rawg.get_game_details(game_slug),
            self.gb.search_game(game_slug.replace("-", " ")),
        )
        if not rawg_detail:
            return None

        screenshots = await self.rawg.get_game_screenshots(game_slug)
        gb_lore = self.gb.extract_lore(gb_game) if gb_game else {}
        themes = gb_lore.get("themes") or []

        sources = ["RAWG"]
        if gb_game:
            sources.append("GiantBomb")

        return GameLoraResponse(
            slug=game_slug,
            name=rawg_detail.get("name", ""),
            description=_strip_html(rawg_detail.get("description") or rawg_detail.get("description_raw")),
            storyline=_strip_html(rawg_detail.get("description_raw")),
            themes=themes,
            lore_summary=_strip_html(gb_lore.get("deck") or gb_lore.get("description")),
            genres=_genres_from_rawg(rawg_detail),
            tags=_tags_from_rawg(rawg_detail),
            cover_image=_cover(rawg_detail) or gb_lore.get("image"),
            screenshots=[Screenshot(url=s["image"]) for s in screenshots if s.get("image")],
            sources=sources,
        )

    # ─────────────────────────────────────────────
    # 3. FRANCHISE TIMELINE
    # ─────────────────────────────────────────────
    async def get_franchise_timeline(self, franchise_name: str) -> Optional[FranchiseTimeline]:
        rawg_games, gb_franchise = await asyncio.gather(
            self.rawg.search_franchise(franchise_name),
            self.gb.search_franchise(franchise_name),
        )

        # Filter RAWG results that match franchise name
        filtered = [
            g for g in rawg_games
            if franchise_name.lower() in g.get("name", "").lower()
        ]
        if not filtered and rawg_games:
            filtered = rawg_games[:10]

        # Sort by release date
        def sort_key(g):
            return g.get("released") or "9999"
        filtered.sort(key=sort_key)

        entries = []
        for i, g in enumerate(filtered, 1):
            entries.append(FranchiseEntry(
                position=i,
                name=g.get("name", ""),
                slug=g.get("slug"),
                release_date=g.get("released"),
                release_year=_parse_year(g.get("released")),
                entry_type=_determine_relation(g, franchise_name),
                platforms=_platforms_from_rawg(g),
                cover_image=_cover(g),
                rating=g.get("rating"),
                short_description=None,
            ))

        if not entries:
            return None

        sources = ["RAWG"]
        if gb_franchise:
            sources.append("GiantBomb")

        return FranchiseTimeline(
            franchise_name=franchise_name,
            total_entries=len(entries),
            entries=entries,
            sources=sources,
        )

    # ─────────────────────────────────────────────
    # 4. STUDIO HISTORY
    # ─────────────────────────────────────────────
    async def get_studio_history(self, studio_name: str) -> Optional[StudioHistory]:
        rawg_dev, gb_company = await asyncio.gather(
            self.rawg.search_developer(studio_name),
            self.gb.search_company(studio_name),
        )
        if not rawg_dev:
            return None

        dev_slug = rawg_dev.get("slug", "")
        rawg_games = await self.rawg.get_developer_games(dev_slug)

        def sort_key(g):
            return g.get("released") or "9999"
        rawg_games.sort(key=sort_key)

        games = []
        for i, g in enumerate(rawg_games, 1):
            games.append(StudioGame(
                position=i,
                name=g.get("name", ""),
                slug=g.get("slug"),
                release_date=g.get("released"),
                release_year=_parse_year(g.get("released")),
                genres=[genre["name"] for genre in (g.get("genres") or [])],
                platforms=_platforms_from_rawg(g),
                rating=g.get("rating"),
                cover_image=_cover(g),
            ))

        sources = ["RAWG"]
        gb_desc = None
        if gb_company:
            sources.append("GiantBomb")
            gb_desc = _strip_html(gb_company.get("deck") or gb_company.get("description"))

        dev_detail = await self.rawg.get_developer_details(dev_slug)

        return StudioHistory(
            studio_name=rawg_dev.get("name", studio_name),
            slug=dev_slug,
            description=gb_desc or _strip_html(dev_detail.get("description") if dev_detail else None),
            total_games=len(games),
            games=games,
            sources=sources,
        )

    # ─────────────────────────────────────────────
    # 5. SUCCESSOR-PREDECESSOR CHAIN
    # ─────────────────────────────────────────────
    async def get_series_chain(self, game_name: str) -> Optional[SuccessorPredecessorMap]:
        rawg_game = await self.rawg.search_game(game_name)
        if not rawg_game:
            return None

        slug = rawg_game.get("slug", "")

        # Try RAWG game-series endpoint
        series_games = await self.rawg.get_game_series(slug)

        # Include the queried game itself
        all_games = [rawg_game] + [g for g in series_games if g.get("slug") != slug]

        # Also try franchise search via GB
        gb_game = await self.gb.search_game(game_name)
        gb_lore = self.gb.extract_lore(gb_game) if gb_game else {}
        series_name = (gb_lore.get("franchises") or [None])[0]

        # If no series found via game-series, fallback to franchise search on RAWG
        if not series_games and series_name:
            franchise_games = await self.rawg.search_franchise(series_name)
            all_games = [g for g in franchise_games if series_name.lower() in g.get("name", "").lower()]
            if not all_games:
                all_games = franchise_games[:15]

        if not all_games:
            # Last resort: return just the game itself
            all_games = [rawg_game]

        # Sort by release date
        def sort_key(g):
            return g.get("released") or "9999"
        all_games.sort(key=sort_key)

        chain: List[SeriesNode] = []
        for i, g in enumerate(all_games):
            prev_name = all_games[i - 1]["name"] if i > 0 else None
            next_name = all_games[i + 1]["name"] if i < len(all_games) - 1 else None
            release = g.get("released")
            chain.append(SeriesNode(
                position=i + 1,
                name=g.get("name", ""),
                slug=g.get("slug"),
                release_year=_parse_year(release),
                release_date=release,
                relation=_determine_relation(g, game_name),
                predecessor=prev_name,
                successor=next_name,
                cover_image=_cover(g),
                platforms=_platforms_from_rawg(g),
            ))

        sources = ["RAWG"]
        if gb_game:
            sources.append("GiantBomb")

        return SuccessorPredecessorMap(
            query_game=game_name,
            series_name=series_name,
            total_entries=len(chain),
            chain=chain,
            sources=sources,
        )

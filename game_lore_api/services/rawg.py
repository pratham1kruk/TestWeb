import httpx
from typing import Optional, Dict, Any, List


RAWG_BASE = "https://api.rawg.io/api"


class RAWGService:
    def __init__(self, client: httpx.AsyncClient, api_key: str):
        self.client = client
        self.api_key = api_key

    def _params(self, **kwargs) -> Dict:
        p = {"key": self.api_key} if self.api_key else {}
        p.update(kwargs)
        return p

    async def search_game(self, name: str) -> Optional[Dict]:
        """Search RAWG for a game by name, return best match."""
        resp = await self.client.get(
            f"{RAWG_BASE}/games",
            params=self._params(search=name, page_size=1, search_precise=True)
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get("results", [])
        return results[0] if results else None

    async def get_game_details(self, slug: str) -> Optional[Dict]:
        """Get full game details from RAWG by slug."""
        resp = await self.client.get(
            f"{RAWG_BASE}/games/{slug}",
            params=self._params()
        )
        if resp.status_code != 200:
            return None
        return resp.json()

    async def get_game_screenshots(self, slug: str) -> List[Dict]:
        resp = await self.client.get(
            f"{RAWG_BASE}/games/{slug}/screenshots",
            params=self._params(page_size=5)
        )
        if resp.status_code != 200:
            return []
        return resp.json().get("results", [])

    async def get_developer_games(self, developer_slug: str) -> List[Dict]:
        """Get all games from a developer, sorted by release date."""
        games = []
        page = 1
        while True:
            resp = await self.client.get(
                f"{RAWG_BASE}/games",
                params=self._params(
                    developers=developer_slug,
                    ordering="released",
                    page_size=40,
                    page=page
                )
            )
            if resp.status_code != 200:
                break
            data = resp.json()
            results = data.get("results", [])
            games.extend(results)
            if not data.get("next") or page >= 5:  # cap at 5 pages / 200 games
                break
            page += 1
        return games

    async def search_developer(self, name: str) -> Optional[Dict]:
        resp = await self.client.get(
            f"{RAWG_BASE}/developers",
            params=self._params(search=name, page_size=1)
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        return results[0] if results else None

    async def get_developer_details(self, slug: str) -> Optional[Dict]:
        resp = await self.client.get(
            f"{RAWG_BASE}/developers/{slug}",
            params=self._params()
        )
        if resp.status_code != 200:
            return None
        return resp.json()

    async def get_game_series(self, slug: str) -> List[Dict]:
        """Get games in the same series as the given game."""
        resp = await self.client.get(
            f"{RAWG_BASE}/games/{slug}/game-series",
            params=self._params(page_size=50)
        )
        if resp.status_code != 200:
            return []
        return resp.json().get("results", [])

    async def search_franchise(self, name: str) -> List[Dict]:
        """Search games in a franchise by franchise name."""
        resp = await self.client.get(
            f"{RAWG_BASE}/games",
            params=self._params(search=name, page_size=20, ordering="-released")
        )
        if resp.status_code != 200:
            return []
        return resp.json().get("results", [])

import httpx
from typing import Optional, Dict, Any, List


GB_BASE = "https://www.giantbomb.com/api"


class GiantBombService:
    def __init__(self, client: httpx.AsyncClient, api_key: str):
        self.client = client
        self.api_key = api_key

    def _headers(self) -> Dict:
        return {"User-Agent": "GameLoreEncyclopediaAPI/1.0"}

    def _params(self, **kwargs) -> Dict:
        p = {
            "api_key": self.api_key,
            "format": "json",
        }
        p.update(kwargs)
        return p

    async def search_game(self, name: str) -> Optional[Dict]:
        """Search GiantBomb for a game by name."""
        if not self.api_key:
            return None
        resp = await self.client.get(
            f"{GB_BASE}/search/",
            params=self._params(
                query=name,
                resources="game",
                field_list="id,name,deck,description,themes,franchises,original_release_date,image,developers,publishers,platforms",
                limit=1,
            ),
            headers=self._headers(),
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        return results[0] if results else None

    async def get_game_by_id(self, game_id: int) -> Optional[Dict]:
        if not self.api_key:
            return None
        resp = await self.client.get(
            f"{GB_BASE}/game/{game_id}/",
            params=self._params(
                field_list="id,name,deck,description,themes,franchises,similar_games,original_release_date,image,developers,publishers,platforms,concepts,genres"
            ),
            headers=self._headers(),
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return None
        return resp.json().get("results")

    async def search_franchise(self, name: str) -> Optional[Dict]:
        """Search for a franchise on GiantBomb."""
        if not self.api_key:
            return None
        resp = await self.client.get(
            f"{GB_BASE}/search/",
            params=self._params(
                query=name,
                resources="franchise",
                field_list="id,name,deck,description,games",
                limit=1,
            ),
            headers=self._headers(),
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        return results[0] if results else None

    async def get_franchise_games(self, franchise_id: int) -> List[Dict]:
        """Get all games in a franchise."""
        if not self.api_key:
            return []
        resp = await self.client.get(
            f"{GB_BASE}/franchise/{franchise_id}/",
            params=self._params(
                field_list="id,name,games,deck"
            ),
            headers=self._headers(),
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return []
        franchise = resp.json().get("results", {})
        return franchise.get("games", [])

    async def search_company(self, name: str) -> Optional[Dict]:
        """Search for a developer/publisher company."""
        if not self.api_key:
            return None
        resp = await self.client.get(
            f"{GB_BASE}/search/",
            params=self._params(
                query=name,
                resources="company",
                field_list="id,name,deck,description,developed_games,country,date_founded",
                limit=1,
            ),
            headers=self._headers(),
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        return results[0] if results else None

    def extract_lore(self, gb_game: Dict) -> Dict:
        """Extract lore-relevant fields from a GiantBomb game object."""
        if not gb_game:
            return {}
        themes = []
        if gb_game.get("themes"):
            themes = [t.get("name", "") for t in gb_game["themes"] if t.get("name")]
        franchises = []
        if gb_game.get("franchises"):
            franchises = [f.get("name", "") for f in gb_game["franchises"] if f.get("name")]
        return {
            "deck": gb_game.get("deck"),          # short description / tagline
            "description": gb_game.get("description"),  # full HTML description
            "themes": themes,
            "franchises": franchises,
            "image": gb_game.get("image", {}).get("original_url"),
        }

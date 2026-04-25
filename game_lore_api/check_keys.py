"""
API Key Checker — run this before starting the server
Usage: python check_keys.py
"""

import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RAWG_KEY = os.getenv("RAWG_API_KEY", "")
GB_KEY = os.getenv("GIANTBOMB_API_KEY", "")

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def ok(msg): print(f"  {GREEN}✅ {msg}{RESET}")
def fail(msg): print(f"  {RED}❌ {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}⚠️  {msg}{RESET}")
def header(msg): print(f"\n{BOLD}{msg}{RESET}")


async def check_rawg(client: httpx.AsyncClient):
    header("━━━ RAWG API ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if not RAWG_KEY:
        warn("RAWG_API_KEY not set in .env — requests may be rate-limited or blocked")
    else:
        ok(f"Key found: {RAWG_KEY[:6]}{'*' * (len(RAWG_KEY)-6)}")

    try:
        resp = await client.get(
            "https://api.rawg.io/api/games",
            params={"key": RAWG_KEY, "search": "doom", "page_size": 3},
            timeout=10
        )

        print(f"  HTTP Status : {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            count = data.get("count", 0)
            results = data.get("results", [])
            names = [g["name"] for g in results]

            if count > 0:
                ok(f"Connection working — {count} results for 'doom'")
                ok(f"Top matches: {', '.join(names)}")
            else:
                fail("Connected but 0 results returned — key may be invalid")
                print(f"  Raw response: {data}")

        elif resp.status_code == 401:
            fail("401 Unauthorized — your RAWG API key is invalid")
        elif resp.status_code == 403:
            fail("403 Forbidden — key rejected or quota exceeded")
        else:
            fail(f"Unexpected status {resp.status_code}")
            print(f"  Response: {resp.text[:300]}")

    except httpx.ConnectError:
        fail("Cannot reach api.rawg.io — check your internet connection")
    except Exception as e:
        fail(f"Exception: {e}")


async def check_giantbomb(client: httpx.AsyncClient):
    header("━━━ GiantBomb API ━━━━━━━━━━━━━━━━━━━━━━━━")

    if not GB_KEY:
        warn("GIANTBOMB_API_KEY not set in .env — lore/themes will return null")
        print("  Get a free key at: https://www.giantbomb.com/api/")
        return
    else:
        ok(f"Key found: {GB_KEY[:6]}{'*' * (len(GB_KEY)-6)}")

    try:
        resp = await client.get(
            "https://www.giantbomb.com/api/search/",
            params={
                "api_key": GB_KEY,
                "format": "json",
                "query": "doom",
                "resources": "game",
                "field_list": "id,name,deck",
                "limit": 3,
            },
            headers={"User-Agent": "GameLoreEncyclopediaAPI/1.0"},
            timeout=10,
            follow_redirects=True,
        )

        print(f"  HTTP Status : {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            status_code = data.get("status_code")
            results = data.get("results", [])
            names = [g["name"] for g in results]

            if status_code == 1:
                ok(f"Connection working — {len(results)} results for 'doom'")
                ok(f"Top matches: {', '.join(names)}")
            elif status_code == 100:
                fail("Invalid API key — GiantBomb rejected it")
            elif status_code == 101:
                fail("Object not found")
            else:
                fail(f"GiantBomb error code {status_code}: {data.get('error')}")

        elif resp.status_code == 401:
            fail("401 Unauthorized — invalid GiantBomb API key")
        else:
            fail(f"Unexpected status {resp.status_code}")
            print(f"  Response: {resp.text[:300]}")

    except httpx.ConnectError:
        fail("Cannot reach www.giantbomb.com — check your internet connection")
    except Exception as e:
        fail(f"Exception: {e}")


async def main():
    print(f"\n{BOLD}🎮 Game Lore API — Key Checker{RESET}")
    print("─" * 45)

    async with httpx.AsyncClient() as client:
        await check_rawg(client)
        await check_giantbomb(client)

    header("━━━ Summary ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    rawg_ok = bool(RAWG_KEY)
    gb_ok = bool(GB_KEY)

    if rawg_ok and gb_ok:
        ok("Both keys set — full API functionality available")
    elif rawg_ok:
        warn("Only RAWG key set — lore/themes will be missing (GiantBomb data null)")
    else:
        fail("No keys set — most endpoints will return 404")
        print(f"\n  {BOLD}Fix:{RESET} Edit your .env file:")
        print("  RAWG_API_KEY=your_key_here      # https://rawg.io/apidocs")
        print("  GIANTBOMB_API_KEY=your_key_here  # https://www.giantbomb.com/api/\n")

    print()


if __name__ == "__main__":
    asyncio.run(main())

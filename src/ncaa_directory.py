"""Scrape NCAA directory for all tennis programs."""

import asyncio
import json
import re
from pathlib import Path

from playwright.async_api import async_playwright
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import Division

console = Console()


async def scrape_ncaa_directory() -> list[dict]:
    """Scrape NCAA directory for all tennis programs across D1, D2, D3."""
    programs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # NCAA Directory URL with tennis filter
        # Sport codes: MTN = Men's Tennis, WTN = Women's Tennis
        base_url = "https://web3.ncaa.org/directory/memberList"

        for division, div_code in [("D1", "1"), ("D2", "2"), ("D3", "3")]:
            for gender, sport_code in [("Men", "MTN"), ("Women", "WTN")]:
                console.print(f"[cyan]Fetching NCAA {division} {gender}'s Tennis programs...[/cyan]")

                # Build URL with filters
                url = f"{base_url}?type=12&division={div_code}&sportCode={sport_code}"

                try:
                    await page.goto(url, timeout=60000)
                    await asyncio.sleep(3)

                    # Wait for table to load
                    await page.wait_for_selector("table tbody tr", timeout=15000)

                    # Extract school data from table
                    rows = await page.query_selector_all("table tbody tr")
                    console.print(f"  Found {len(rows)} programs")

                    for row in rows:
                        try:
                            # Get school name and link
                            name_cell = await row.query_selector("td:first-child a")
                            if not name_cell:
                                continue

                            school_name = await name_cell.inner_text()
                            school_link = await name_cell.get_attribute("href")

                            # Get state (usually in another column)
                            cells = await row.query_selector_all("td")
                            state = ""
                            if len(cells) >= 3:
                                state = await cells[2].inner_text()

                            # Get conference
                            conference = ""
                            if len(cells) >= 2:
                                conference = await cells[1].inner_text()

                            programs.append({
                                "school": school_name.strip(),
                                "state": state.strip(),
                                "conference": conference.strip(),
                                "division": division,
                                "gender": gender,
                                "ncaa_link": school_link,
                            })
                        except Exception as e:
                            continue

                except Exception as e:
                    console.print(f"  [red]Error: {e}[/red]")

                await asyncio.sleep(1)

        await browser.close()

    return programs


async def scrape_ncaa_school_athletics_url(ncaa_url: str, page) -> str | None:
    """From an NCAA school page, find the athletics website URL."""
    try:
        await page.goto(f"https://web3.ncaa.org{ncaa_url}", timeout=30000)
        await asyncio.sleep(2)

        # Look for athletics website link
        links = await page.query_selector_all("a")
        for link in links:
            text = await link.inner_text()
            href = await link.get_attribute("href")
            if href and ("athletics" in text.lower() or "sports" in text.lower()):
                return href

        # Fallback: look for any external link that looks like athletics
        for link in links:
            href = await link.get_attribute("href") or ""
            if "athletics" in href or "gostanford" in href or "sports" in href:
                return href

    except Exception:
        pass

    return None


async def build_university_list():
    """Build complete university list with athletics URLs."""
    console.print("[bold]Building NCAA Tennis Programs Database[/bold]\n")

    # Step 1: Get all programs from NCAA directory
    programs = await scrape_ncaa_directory()

    console.print(f"\n[green]Found {len(programs)} total tennis programs[/green]")

    # Deduplicate by school (each school may have both men's and women's)
    schools = {}
    for prog in programs:
        school = prog["school"]
        if school not in schools:
            schools[school] = {
                "school": school,
                "state": prog["state"],
                "conference": prog["conference"],
                "division": prog["division"],
                "ncaa_link": prog["ncaa_link"],
                "has_mens": False,
                "has_womens": False,
            }
        if prog["gender"] == "Men":
            schools[school]["has_mens"] = True
        else:
            schools[school]["has_womens"] = True

    console.print(f"[green]Unique schools: {len(schools)}[/green]")

    # Save intermediate results
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "ncaa_tennis_schools.json", "w") as f:
        json.dump(list(schools.values()), f, indent=2)

    console.print(f"[green]Saved to data/ncaa_tennis_schools.json[/green]")

    return list(schools.values())


if __name__ == "__main__":
    asyncio.run(build_university_list())

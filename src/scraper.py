"""Core scraping logic for tennis programs with headless browser support."""

import asyncio
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Page

from .models import Coach, Division, Gender, TennisProgram


def extract_email_from_mailto(href: str) -> str | None:
    """Extract email from a mailto: href."""
    if not href or "mailto:" not in href.lower():
        return None
    email = href.lower().replace("mailto:", "").split("?")[0].strip()
    if "@" in email and "." in email.split("@")[1]:
        return email
    return None


def extract_phone_from_tel(href: str) -> str | None:
    """Extract phone from a tel: href."""
    if not href or "tel:" not in href.lower():
        return None
    return href.replace("tel:", "").strip()


def looks_like_person_name(text: str) -> bool:
    """Check if text looks like a person's name."""
    if not text or len(text) < 3 or len(text) > 60:
        return False

    skip_patterns = [
        "head coach", "assistant", "volunteer", "director", "coach",
        "read more", "view bio", "click", "loading", "staff",
        "email", "phone", "office", "fax", "schedule", "roster",
        "news", "tickets", "donate", "contact", "twitter", "instagram",
        "facebook", "youtube", "tiktok", "print", "share",
    ]
    lower = text.lower()
    if any(p in lower for p in skip_patterns):
        return False

    words = text.split()
    if len(words) < 2:
        return False

    if not all(w[0].isupper() for w in words if w):
        return False

    return True


class TennisScraper:
    def __init__(self, rate_limit: float = 1.5):
        self.rate_limit = rate_limit
        self.browser: Browser | None = None
        self.playwright = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self

    async def __aexit__(self, *args):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def fetch_with_js(self, url: str, wait_for: str | None = None) -> str | None:
        """Fetch a URL using headless browser, waiting for JS to render."""
        await asyncio.sleep(self.rate_limit)
        page: Page | None = None
        try:
            page = await self.browser.new_page()
            await page.goto(url, timeout=30000)

            # Wait for content to load
            if wait_for:
                try:
                    await page.wait_for_selector(wait_for, timeout=5000)
                except:
                    pass
            else:
                # Wait for network to be mostly idle
                await page.wait_for_load_state("networkidle", timeout=10000)

            # Small additional wait for any final renders
            await asyncio.sleep(0.5)

            return await page.content()
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            return None
        finally:
            if page:
                await page.close()

    async def check_url_exists(self, url: str) -> bool:
        """Check if a URL exists (returns 200)."""
        page: Page | None = None
        try:
            page = await self.browser.new_page()
            response = await page.goto(url, timeout=15000)
            return response is not None and response.status == 200
        except:
            return False
        finally:
            if page:
                await page.close()

    def get_tennis_sport_paths(self, gender: Gender) -> list[str]:
        """Get common sport path patterns for tennis."""
        if gender == Gender.MEN:
            return [
                "/sports/mens-tennis",
                "/sports/m-tennis",
                "/sports/mten",     # Kentucky, some SEC sites
                "/sport/m-tennis",  # Arkansas, Auburn, etc.
                "/m-tennis",
            ]
        else:
            return [
                "/sports/womens-tennis",
                "/sports/w-tennis",
                "/sports/wten",     # Kentucky, some SEC sites
                "/sport/w-tennis",  # Arkansas, Auburn, etc.
                "/w-tennis",
            ]

    async def find_tennis_page(self, athletics_url: str, gender: Gender) -> str | None:
        """Find the tennis team page URL."""
        base = athletics_url.rstrip("/")

        for path in self.get_tennis_sport_paths(gender):
            url = f"{base}{path}"
            if await self.check_url_exists(url):
                return url

        return None

    async def find_coaches_url(self, tennis_url: str) -> str | None:
        """Find the coaches page URL."""
        base_url = tennis_url.rstrip("/")

        for pattern in ["/coaches", "/staff", "/roster/coaches", "/roster/#coaches"]:
            url = f"{base_url}{pattern}"
            if await self.check_url_exists(url):
                return url

        return None

    async def scrape_roster_coaches_section(self, tennis_url: str) -> tuple[Coach | None, list[Coach]]:
        """Scrape coaches from roster page with #coaches section or coach tables."""
        # Build list of potential roster URLs to try
        roster_urls = [f"{tennis_url.rstrip('/')}/roster/"]

        # Try alternate URL patterns
        # Arkansas uses /sport/ instead of /sports/
        if "/sports/" in tennis_url:
            roster_urls.append(tennis_url.replace("/sports/", "/sport/").rstrip('/') + "/roster/")

        # Kentucky uses mten/wten instead of mens-tennis/womens-tennis
        if "mens-tennis" in tennis_url:
            roster_urls.append(tennis_url.replace("mens-tennis", "mten").rstrip('/') + "/roster/")
        elif "womens-tennis" in tennis_url:
            roster_urls.append(tennis_url.replace("womens-tennis", "wten").rstrip('/') + "/roster/")

        page: Page | None = None
        try:
            page = await self.browser.new_page()

            html = None
            # Try each roster URL until we find one with coach data
            for roster_url in roster_urls:
                try:
                    await page.goto(roster_url, timeout=30000)
                    await asyncio.sleep(2)

                    # Look for coaches section by ID
                    coaches_section = await page.query_selector("#coaches")
                    if coaches_section:
                        html = await coaches_section.inner_html()
                        break

                    # Fallback: Check for coach table on roster page (Kentucky-style)
                    full_html = await page.content()
                    if "head coach" in full_html.lower():
                        html = full_html
                        break
                except:
                    continue

            if not html:
                return None, []

            # Parse the coaches section
            soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
            coaches: list[Coach] = []
            seen_names: set[str] = set()

            # Look for table rows (Arkansas pattern)
            rows = soup.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                    continue

                name = None
                title = None
                email = None

                # First cell usually has name with link
                name_cell = cells[0]
                name_link = name_cell.find("a")
                if name_link:
                    name = name_link.get_text(strip=True)
                else:
                    name = name_cell.get_text(strip=True)

                if not name or not looks_like_person_name(name):
                    continue

                # Second cell usually has title
                if len(cells) >= 2:
                    title = cells[1].get_text(strip=True)

                # Look for email in the row
                mailto = row.find("a", href=re.compile(r"^mailto:", re.I))
                if mailto:
                    email = extract_email_from_mailto(mailto["href"])

                if name not in seen_names:
                    seen_names.add(name)
                    coaches.append(Coach(name=name, title=title, email=email, phone=None))

            # Separate head coach from assistants
            head_coach = None
            assistants = []

            for coach in coaches:
                is_head = coach.title and (
                    "head coach" in coach.title.lower()
                    and "assistant" not in coach.title.lower()
                    and "associate" not in coach.title.lower()
                )
                if is_head and not head_coach:
                    head_coach = coach
                else:
                    assistants.append(coach)

            return head_coach, assistants

        except Exception as e:
            print(f"  Error fetching roster coaches: {e}")
            return None, []
        finally:
            if page:
                await page.close()

    def parse_coaches_from_html(self, html: str, base_url: str) -> tuple[Coach | None, list[Coach]]:
        """Parse coach information from rendered HTML."""
        soup = BeautifulSoup(html, "lxml")
        coaches: list[Coach] = []
        seen_names: set[str] = set()

        # Strategy 1: Parse table rows (common on newer Sidearm sites)
        # Look for tables or table-like structures with coach data
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    coach = self._extract_coach_from_row(cells)
                    if coach and coach.name not in seen_names:
                        seen_names.add(coach.name)
                        coaches.append(coach)

        # Strategy 2: Look for coach cards (common Sidearm patterns)
        if not coaches:
            coach_cards = soup.select(
                ".sidearm-coaches-coach, "
                "[class*='coach-card'], "
                "[class*='staff-card'], "
                "[class*='person-card'], "
                "article[class*='coach'], "
                "li[class*='coach']"
            )

            for card in coach_cards:
                coach = self._extract_coach_from_card(card)
                if coach and coach.name not in seen_names:
                    seen_names.add(coach.name)
                    coaches.append(coach)

        # Strategy 3: Look for staff links and extract info
        if not coaches:
            staff_links = soup.find_all("a", href=re.compile(r"/staff/[a-zA-Z0-9-]+", re.I))
            for link in staff_links[:15]:
                name = link.get_text(strip=True)
                if looks_like_person_name(name) and name not in seen_names:
                    seen_names.add(name)

                    parent = link.find_parent(["div", "li", "article", "section", "tr"])
                    email = None
                    title = None
                    phone = None

                    if parent:
                        mailto = parent.find("a", href=re.compile(r"^mailto:", re.I))
                        if mailto:
                            email = extract_email_from_mailto(mailto["href"])

                        tel = parent.find("a", href=re.compile(r"^tel:", re.I))
                        if tel:
                            phone = extract_phone_from_tel(tel["href"])

                        # Look for title
                        parent_text = parent.get_text()
                        for pattern in ["Head Coach", "Assistant Coach", "Associate Head Coach", "Volunteer"]:
                            if pattern.lower() in parent_text.lower():
                                title = pattern
                                break

                    coaches.append(Coach(name=name, title=title, email=email, phone=phone))

        # Strategy 4: Match emails to names via context text
        if not coaches:
            mailto_links = soup.find_all("a", href=re.compile(r"^mailto:", re.I))

            for mailto in mailto_links[:15]:
                email = extract_email_from_mailto(mailto["href"])
                if not email:
                    continue

                # Get surrounding context - walk up to find a container
                parent = mailto.find_parent(["div", "li", "article", "tr", "section"])
                if not parent:
                    continue

                parent_text = parent.get_text(separator=" ", strip=True)

                # Try to find name and title in the text
                name, title = self._extract_name_title_from_text(parent_text)

                if name and name not in seen_names:
                    seen_names.add(name)
                    coaches.append(Coach(name=name, title=title, email=email, phone=None))

        # Separate head coach from assistants
        head_coach = None
        assistants = []

        for coach in coaches:
            is_head = coach.title and (
                "head coach" in coach.title.lower()
                and "assistant" not in coach.title.lower()
                and "associate" not in coach.title.lower()
            )
            if is_head and not head_coach:
                head_coach = coach
            else:
                assistants.append(coach)

        return head_coach, assistants

    def _extract_coach_from_row(self, cells) -> Coach | None:
        """Extract coach info from a table row."""
        if len(cells) < 2:
            return None

        name = None
        title = None
        email = None
        phone = None

        for cell in cells:
            text = cell.get_text(strip=True)

            # Check for email link
            mailto = cell.find("a", href=re.compile(r"^mailto:", re.I))
            if mailto:
                email = extract_email_from_mailto(mailto["href"])
                continue

            # Check for phone
            tel = cell.find("a", href=re.compile(r"^tel:", re.I))
            if tel:
                phone = extract_phone_from_tel(tel["href"])
                continue

            # Check if it looks like a name first (before title check)
            if looks_like_person_name(text) and not name:
                name = text
                continue

            # Check if it's a title - must contain space and coaching keyword
            # Avoid matching social media handles like "coachjamiehunt"
            if " " in text and any(t in text.lower() for t in ["coach", "director", "coordinator"]):
                title = text
                continue

        if not name:
            return None

        return Coach(name=name, title=title, email=email, phone=phone)

    def _extract_name_title_from_text(self, text: str) -> tuple[str | None, str | None]:
        """Extract name and title from a text block."""
        # Common patterns: "John Smith Head Coach" or "Head Coach John Smith"
        title_patterns = [
            r"(Head Coach)",
            r"(Associate Head Coach)",
            r"(Assistant Coach)",
            r"(Volunteer Assistant)",
            r"(Director of Tennis)",
            r"(Strength and Conditioning Coach[^,]*)",
        ]

        title = None
        for pattern in title_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                title = match.group(1)
                break

        # Try to find a name (2+ capitalized words in sequence)
        name_match = re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", text)
        name = None
        if name_match:
            potential_name = name_match.group(1)
            # Make sure it's not just the title
            if title and potential_name.lower() == title.lower():
                # Try to find another name
                remaining = text.replace(potential_name, "", 1)
                name_match = re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", remaining)
                if name_match:
                    name = name_match.group(1)
            else:
                name = potential_name

        return name, title

    def _extract_coach_from_card(self, card) -> Coach | None:
        """Extract coach info from a card element."""
        # Find name
        name = None
        name_selectors = [
            ".sidearm-coaches-coach-name",
            "[class*='name']",
            "h2", "h3", "h4",
            "a[href*='/staff/']",
        ]

        for selector in name_selectors:
            elem = card.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if looks_like_person_name(text):
                    name = text
                    break

        if not name:
            return None

        # Find title
        title = None
        title_selectors = [
            ".sidearm-coaches-coach-title",
            "[class*='title']",
            "[class*='position']",
        ]

        for selector in title_selectors:
            elem = card.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                if "coach" in text.lower() or "director" in text.lower():
                    title = text
                    break

        if not title:
            # Look in card text for coach keywords
            card_text = card.get_text()
            for pattern in [r"(Head Coach)", r"(Assistant Coach)", r"(Associate Head Coach)"]:
                match = re.search(pattern, card_text, re.I)
                if match:
                    title = match.group(1)
                    break

        # Find email
        email = None
        mailto = card.find("a", href=re.compile(r"^mailto:", re.I))
        if mailto:
            email = extract_email_from_mailto(mailto["href"])

        # Find phone
        phone = None
        tel = card.find("a", href=re.compile(r"^tel:", re.I))
        if tel:
            phone = extract_phone_from_tel(tel["href"])

        return Coach(name=name, title=title, email=email, phone=phone)

    async def scrape_coaches_page(self, coaches_url: str) -> tuple[Coach | None, list[Coach]]:
        """Scrape coach information using headless browser."""
        html = await self.fetch_with_js(
            coaches_url,
            wait_for="a[href*='mailto:'], [class*='coach'], [class*='staff']"
        )

        if not html:
            return None, []

        return self.parse_coaches_from_html(html, coaches_url)

    async def scrape_stanford_staff_directory(self, gender: Gender) -> tuple[Coach | None, list[Coach]]:
        """Special handler for Stanford's centralized staff directory."""
        sport_filter = "men's tennis" if gender == Gender.MEN else "women's tennis"
        url = "https://gostanford.com/staff-directory"

        html = await self.fetch_with_js(url)
        if not html:
            return None, []

        soup = BeautifulSoup(html, "lxml")
        coaches: list[Coach] = []
        seen_names: set[str] = set()

        # Stanford has table rows with staff info
        # Format: Name | Title | Email | Phone
        rows = soup.find_all("tr")

        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue

            row_text = row.get_text().lower()

            # Check if this row is for our tennis sport (exclusive, not shared with other sports)
            # Look specifically for tennis coaching titles, not support staff
            sport_specific = "men's tennis" if gender == Gender.MEN else "women's tennis"
            is_tennis_coach = (
                sport_specific in row_text and
                # Must have director/coach in title context, not just in sport list
                (
                    f"director of {sport_specific}" in row_text or
                    f"director • {sport_specific}" in row_text or
                    f"{sport_specific} assistant coach" in row_text or
                    f"assistant {sport_specific} coach" in row_text or
                    f"{sport_specific} coach" in row_text or
                    "head coach" in row_text
                )
            )

            # Also try Stanford's endowed position pattern
            if not is_tennis_coach:
                is_tennis_coach = (
                    sport_specific in row_text and
                    ("director" in row_text or "coach" in row_text) and
                    ("taube" in row_text or "family" in row_text or "endowed" in row_text)
                )

            if not is_tennis_coach:
                continue

            # Extract name (usually first cell or first link)
            name = None
            name_link = row.find("a", href=re.compile(r"/staff/", re.I))
            if name_link:
                name = name_link.get_text(strip=True)
            elif cells:
                name = cells[0].get_text(strip=True)

            if not name or name in seen_names or len(name) < 3:
                continue

            # Skip if name contains non-name words
            name_lower = name.lower()
            if any(skip in name_lower for skip in ["email", "phone", "office", "staff directory"]):
                continue

            seen_names.add(name)

            # Extract title
            title = None
            for cell in cells[1:]:
                cell_text = cell.get_text(strip=True)
                if "director" in cell_text.lower() or "coach" in cell_text.lower():
                    title = cell_text
                    break

            # Extract email
            email = None
            mailto = row.find("a", href=re.compile(r"^mailto:", re.I))
            if mailto:
                email = extract_email_from_mailto(mailto["href"])

            # Determine if this is the head coach
            # Stanford uses "Director of Men's/Women's Tennis" for head coach
            is_head = title and (
                "director of" in title.lower() and "tennis" in title.lower() and "assistant" not in title.lower()
            )

            coach = Coach(name=name, title=title, email=email, phone=None)

            if is_head:
                # Return immediately as head coach
                assistants = [c for c in coaches]  # Previous coaches are assistants
                return coach, assistants

            coaches.append(coach)

        # If no head coach found, first coach might be head
        head_coach = None
        assistants = coaches

        if coaches:
            # The first tennis-specific staff member is likely the head coach
            head_coach = coaches[0]
            assistants = coaches[1:]

        return head_coach, assistants

    async def scrape_virginia_roster(self, tennis_url: str) -> tuple[Coach | None, list[Coach]]:
        """Special handler for Virginia's roster page with coaches section."""
        roster_url = f"{tennis_url.rstrip('/')}/roster/"

        page: Page | None = None
        try:
            page = await self.browser.new_page()
            await page.goto(roster_url, timeout=30000)
            await asyncio.sleep(2)

            # Click on coaches tab if it exists
            coaches_tab = await page.query_selector("a[href*='#coaches'], button:has-text('Coaches')")
            if coaches_tab:
                await coaches_tab.click()
                await asyncio.sleep(1)

            html = await page.content()
        except Exception as e:
            print(f"  Error fetching Virginia roster: {e}")
            return None, []
        finally:
            if page:
                await page.close()

        if not html:
            return None, []

        return self.parse_coaches_from_html(html, roster_url)

    def get_site_type(self, athletics_url: str) -> str:
        """Determine site type for special handling."""
        url_lower = athletics_url.lower()
        if "gostanford.com" in url_lower:
            return "stanford"
        elif "virginiasports.com" in url_lower:
            return "virginia"
        return "standard"

    async def scrape_program(
        self,
        university: str,
        state: str,
        athletics_url: str,
        division: Division,
        gender: Gender,
    ) -> TennisProgram:
        """Scrape a complete tennis program."""
        tennis_url = await self.find_tennis_page(athletics_url, gender)

        head_coach = None
        assistants = []

        site_type = self.get_site_type(athletics_url)

        if site_type == "stanford":
            # Stanford uses centralized staff directory
            head_coach, assistants = await self.scrape_stanford_staff_directory(gender)
        elif site_type == "virginia" and tennis_url:
            # Virginia has coaches on roster page
            head_coach, assistants = await self.scrape_virginia_roster(tennis_url)
            # Fallback to standard if no results
            if not head_coach and not assistants:
                coaches_url = await self.find_coaches_url(tennis_url)
                if coaches_url:
                    head_coach, assistants = await self.scrape_coaches_page(coaches_url)
        elif tennis_url:
            # Standard approach
            coaches_url = await self.find_coaches_url(tennis_url)
            if coaches_url:
                head_coach, assistants = await self.scrape_coaches_page(coaches_url)

            # Fallback: Try roster page with #coaches section (Arkansas, Auburn, LSU, etc.)
            if not head_coach and not assistants:
                head_coach, assistants = await self.scrape_roster_coaches_section(tennis_url)

        team_name = f"{'Men' if gender == Gender.MEN else 'Women'}'s Tennis"

        return TennisProgram(
            university=university,
            state=state,
            division=division,
            gender=gender,
            team_name=team_name,
            head_coach=head_coach,
            assistant_coaches=assistants,
            athletics_url=athletics_url,
            tennis_page_url=tennis_url,
        )

"""Data models for tennis program scraper."""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class Division(str, Enum):
    NCAA_D1 = "NCAA D1"
    NCAA_D2 = "NCAA D2"
    NCAA_D3 = "NCAA D3"
    NAIA = "NAIA"
    NJCAA = "NJCAA"


class Gender(str, Enum):
    MEN = "Men"
    WOMEN = "Women"


class Coach(BaseModel):
    name: str
    title: str | None = None
    email: str | None = None
    phone: str | None = None


class TennisProgram(BaseModel):
    university: str
    state: str
    division: Division
    gender: Gender
    team_name: str | None = None
    head_coach: Coach | None = None
    assistant_coaches: list[Coach] = Field(default_factory=list)
    athletics_url: str
    tennis_page_url: str | None = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    def to_flat_dict(self) -> dict:
        """Flatten for CSV export."""
        return {
            "university": self.university,
            "state": self.state,
            "division": self.division.value,
            "gender": self.gender.value,
            "team_name": self.team_name,
            "head_coach_name": self.head_coach.name if self.head_coach else None,
            "head_coach_email": self.head_coach.email if self.head_coach else None,
            "head_coach_phone": self.head_coach.phone if self.head_coach else None,
            "assistant_coaches": "; ".join(
                f"{c.name} ({c.email or 'no email'})" for c in self.assistant_coaches
            ),
            "athletics_url": self.athletics_url,
            "tennis_page_url": self.tennis_page_url,
            "scraped_at": self.scraped_at.isoformat(),
        }

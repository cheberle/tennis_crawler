"""Main entry point for tennis scraper."""

import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .models import Division, Gender, TennisProgram
from .scraper import TennisScraper


console = Console()

# Sample universities for proof-of-concept (NCAA D1)
SAMPLE_UNIVERSITIES = [
    {
        "university": "Stanford University",
        "state": "California",
        "athletics_url": "https://gostanford.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "University of Florida",
        "state": "Florida",
        "athletics_url": "https://floridagators.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "University of Texas",
        "state": "Texas",
        "athletics_url": "https://texassports.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "University of Georgia",
        "state": "Georgia",
        "athletics_url": "https://georgiadogs.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "University of Virginia",
        "state": "Virginia",
        "athletics_url": "https://virginiasports.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "Ohio State University",
        "state": "Ohio",
        "athletics_url": "https://ohiostatebuckeyes.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "UCLA",
        "state": "California",
        "athletics_url": "https://uclabruins.com",
        "division": Division.NCAA_D1,
    },
    {
        "university": "University of Michigan",
        "state": "Michigan",
        "athletics_url": "https://mgoblue.com",
        "division": Division.NCAA_D1,
    },
]


async def scrape_sample_programs() -> list[TennisProgram]:
    """Scrape sample universities for proof-of-concept."""
    programs = []

    async with TennisScraper(rate_limit=2.0) as scraper:
        for uni in SAMPLE_UNIVERSITIES:
            for gender in [Gender.MEN, Gender.WOMEN]:
                console.print(f"[cyan]Scraping {uni['university']} - {gender.value}...[/cyan]")

                try:
                    program = await scraper.scrape_program(
                        university=uni["university"],
                        state=uni["state"],
                        athletics_url=uni["athletics_url"],
                        division=uni["division"],
                        gender=gender,
                    )
                    programs.append(program)

                    # Status update
                    if program.head_coach:
                        console.print(
                            f"  [green]✓[/green] Head Coach: {program.head_coach.name}"
                        )
                    else:
                        console.print(f"  [yellow]⚠[/yellow] No head coach found")

                except Exception as e:
                    console.print(f"  [red]✗ Error: {e}[/red]")

    return programs


def export_to_json(programs: list[TennisProgram], path: Path):
    """Export programs to JSON."""
    data = [p.model_dump(mode="json") for p in programs]
    path.write_text(json.dumps(data, indent=2, default=str))
    console.print(f"[green]Exported {len(programs)} programs to {path}[/green]")


def export_to_csv(programs: list[TennisProgram], path: Path):
    """Export programs to CSV (flattened)."""
    if not programs:
        return

    rows = [p.to_flat_dict() for p in programs]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    console.print(f"[green]Exported {len(programs)} programs to {path}[/green]")


def display_results(programs: list[TennisProgram]):
    """Display results in a table."""
    table = Table(title="Tennis Programs Scraped")

    table.add_column("University", style="cyan")
    table.add_column("Gender")
    table.add_column("Division")
    table.add_column("Head Coach", style="green")
    table.add_column("Email")
    table.add_column("Assistants")

    for p in programs:
        table.add_row(
            p.university,
            p.gender.value,
            p.division.value,
            p.head_coach.name if p.head_coach else "-",
            p.head_coach.email if p.head_coach else "-",
            str(len(p.assistant_coaches)),
        )

    console.print(table)


async def main():
    console.print("[bold]Tennis Program Scraper - Proof of Concept[/bold]\n")

    programs = await scrape_sample_programs()

    # Display results
    console.print("\n")
    display_results(programs)

    # Export
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_to_json(programs, output_dir / f"tennis_programs_{timestamp}.json")
    export_to_csv(programs, output_dir / f"tennis_programs_{timestamp}.csv")

    # Summary stats
    total_with_coach = sum(1 for p in programs if p.head_coach)
    total_with_email = sum(1 for p in programs if p.head_coach and p.head_coach.email)

    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total programs: {len(programs)}")
    console.print(f"  With head coach: {total_with_coach}")
    console.print(f"  With email: {total_with_email}")


if __name__ == "__main__":
    asyncio.run(main())

"""Batch scraper for all NCAA tennis programs."""

import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from .models import Division, Gender, TennisProgram
from .scraper import TennisScraper
from .schools_data import get_all_schools


console = Console()


async def scrape_all_programs(
    limit: int | None = None,
    resume_from: int = 0,
    output_dir: Path = Path("data"),
):
    """Scrape all NCAA tennis programs."""
    output_dir.mkdir(exist_ok=True)

    schools = get_all_schools()
    if limit:
        schools = schools[:limit]

    total_tasks = len(schools) * 2  # Men and Women for each school
    programs: list[TennisProgram] = []
    errors: list[dict] = []

    # Load existing results if resuming
    results_file = output_dir / "all_programs_progress.json"
    if resume_from > 0 and results_file.exists():
        with open(results_file) as f:
            saved = json.load(f)
            programs = [TennisProgram(**p) for p in saved.get("programs", [])]
            errors = saved.get("errors", [])
        console.print(f"[yellow]Resuming from school {resume_from}, loaded {len(programs)} existing programs[/yellow]")

    console.print(f"[bold]Scraping {len(schools)} schools ({total_tasks} programs)[/bold]\n")

    async with TennisScraper(rate_limit=1.0) as scraper:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Scraping...", total=len(schools) - resume_from)

            for i, school in enumerate(schools[resume_from:], start=resume_from):
                progress.update(task, description=f"[cyan]{school['school']}[/cyan]")

                for gender in [Gender.MEN, Gender.WOMEN]:
                    try:
                        program = await scraper.scrape_program(
                            university=school["school"],
                            state=school["state"],
                            athletics_url=school["athletics_url"],
                            division=school["division"],
                            gender=gender,
                        )
                        programs.append(program)

                        if program.head_coach:
                            console.print(f"  ✓ {gender.value}: {program.head_coach.name}")
                        else:
                            console.print(f"  ⚠ {gender.value}: No coach found")

                    except Exception as e:
                        errors.append({
                            "school": school["school"],
                            "gender": gender.value,
                            "error": str(e),
                        })
                        console.print(f"  ✗ {gender.value}: {e}")

                progress.advance(task)

                # Save progress every 10 schools
                if (i + 1) % 10 == 0:
                    save_progress(programs, errors, output_dir)
                    console.print(f"[dim]Progress saved ({i + 1}/{len(schools)} schools)[/dim]")

    # Final save
    save_progress(programs, errors, output_dir)

    # Export final results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_results(programs, output_dir, timestamp)

    # Summary
    display_summary(programs, errors)

    return programs


def save_progress(programs: list[TennisProgram], errors: list[dict], output_dir: Path):
    """Save progress to JSON for resume capability."""
    with open(output_dir / "all_programs_progress.json", "w") as f:
        json.dump({
            "programs": [p.model_dump(mode="json") for p in programs],
            "errors": errors,
            "timestamp": datetime.now().isoformat(),
        }, f, indent=2, default=str)


def export_results(programs: list[TennisProgram], output_dir: Path, timestamp: str):
    """Export results to JSON and CSV."""
    # JSON
    json_path = output_dir / f"all_tennis_programs_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump([p.model_dump(mode="json") for p in programs], f, indent=2, default=str)
    console.print(f"[green]Exported {len(programs)} programs to {json_path}[/green]")

    # CSV
    csv_path = output_dir / f"all_tennis_programs_{timestamp}.csv"
    if programs:
        rows = [p.to_flat_dict() for p in programs]
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        console.print(f"[green]Exported {len(programs)} programs to {csv_path}[/green]")


def display_summary(programs: list[TennisProgram], errors: list[dict]):
    """Display scraping summary."""
    table = Table(title="Scraping Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    total = len(programs)
    with_coach = sum(1 for p in programs if p.head_coach)
    with_email = sum(1 for p in programs if p.head_coach and p.head_coach.email)
    with_phone = sum(1 for p in programs if p.head_coach and p.head_coach.phone)

    table.add_row("Total programs", str(total))
    table.add_row("With head coach", f"{with_coach} ({100*with_coach//total if total else 0}%)")
    table.add_row("With email", f"{with_email} ({100*with_email//total if total else 0}%)")
    table.add_row("With phone", f"{with_phone} ({100*with_phone//total if total else 0}%)")
    table.add_row("Errors", str(len(errors)))

    console.print("\n")
    console.print(table)


async def main():
    """Run the batch scraper."""
    import argparse

    parser = argparse.ArgumentParser(description="Scrape NCAA tennis programs")
    parser.add_argument("--limit", type=int, help="Limit number of schools to scrape")
    parser.add_argument("--resume", type=int, default=0, help="Resume from school index")
    args = parser.parse_args()

    await scrape_all_programs(limit=args.limit, resume_from=args.resume)


if __name__ == "__main__":
    asyncio.run(main())

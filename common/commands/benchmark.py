from dataclasses import dataclass
from typing import Any, List, Optional

import click
from colorama import Fore, Style
from numpy import percentile

from common.format import format_time
from common.runners.run import BenchRun


@dataclass
class BenchmarkResult(BenchRun):
    year: int
    day: int
    part: str


def print_day_header(year: int, day: int) -> None:
    """Print the header for a specific day's benchmarks."""

    click.echo(f"\n{Fore.YELLOW}Year {year}, Day {day}{Style.RESET_ALL}")


def print_group_header(file_name: str) -> None:
    """Print the header for a group of benchmarks."""

    header = (
        f"{'benchmark':20} {'time (avg)':>20} {'p75':>15} {'p99':>15} "
        f"{'(min … max)':>35}"
    )
    separator = "─" * 115

    click.echo(f"\n{Fore.GREEN}• {file_name}{Style.RESET_ALL}")
    click.echo(f"{Fore.WHITE}{header}{Style.RESET_ALL}")
    click.echo(f"{Fore.LIGHTBLACK_EX}{separator}{Style.RESET_ALL}")


def find_faster_part(group_runs: list[Any]) -> tuple[Optional[Any], Optional[float]]:
    """Determine which part is faster and calculate the ratio."""

    if len(group_runs) != 2:
        return None, None

    part1, part2 = group_runs
    part1_avg = part1.avg()
    part2_avg = part2.avg()

    if part1_avg and part2_avg:
        faster_part = part1 if part1_avg < part2_avg else part2
        ratio = max(part1_avg, part2_avg) / min(part1_avg, part2_avg)
        return faster_part, ratio

    return None, None


def format_benchmark_line(
    run: Any, faster_part: Any, ratio: Optional[float]
) -> tuple[str, str]:
    """Format a single benchmark line with comparison."""

    avg_time = run.format_time(run.avg())
    p75_time = run.format_time(run.p(0.75))
    p99_time = run.format_time(run.p(0.99))
    min_time = run.format_time(run.min())
    max_time = run.format_time(run.max())

    benchmark_line = (
        f"{run.beauty_func_name():20} {avg_time:>20}/iter {p75_time:>15} {p99_time:>15} "
        f"{f'({min_time} … {max_time})':>35}"
    )

    color = Fore.CYAN if faster_part and run == faster_part else Fore.WHITE

    return benchmark_line, color


def process_day_benchmarks(
    year: int, day: int, runs: List[BenchRun]
) -> List[BenchmarkResult]:
    """Process benchmarks for a single day."""

    results = []
    groups = {}
    for run in runs:
        groups.setdefault(run.file_name, []).append(run)

    print_day_header(year, day)

    for file_name, group_runs in groups.items():
        print_group_header(file_name)
        faster_part, ratio = find_faster_part(group_runs)

        for run in group_runs:
            benchmark_line, color = format_benchmark_line(run, faster_part, ratio)
            click.echo(f"{color}{benchmark_line}{Style.RESET_ALL}")

            results.append(
                BenchmarkResult(
                    year=year,
                    day=day,
                    part=run.beauty_func_name(),
                    func_name=run.func_name,
                    times=run.times,
                    file_name=run.file_name,
                )
            )

        click.echo()

    return results


def print_performance_overview(results: List[BenchmarkResult]) -> None:
    """Print the overall performance summary."""
    total_time = sum(r.avg() for r in results)

    click.echo(f"{Fore.CYAN}🏃 Performance Overview{Style.RESET_ALL}")
    click.echo(f"Total execution time: {format_time(total_time)}")
    click.echo(f"Average per puzzle: {format_time(total_time / len(results))}\n")


def print_fastest_slowest(results: List[BenchmarkResult]) -> None:
    """Print the fastest and slowest solutions."""
    results = sorted(results, key=lambda x: x.avg())

    fastest = results[0]
    slowest = results[-1]

    click.echo(f"{Fore.GREEN}⚡ Fastest Solution{Style.RESET_ALL}")
    click.echo(f"Day {fastest.day} {fastest.part}: {format_time(fastest.avg())}/iter")

    click.echo(f"\n{Fore.RED}🐌 Slowest Solution{Style.RESET_ALL}")
    click.echo(f"Day {slowest.day} {slowest.part}: {format_time(slowest.avg())}/iter")


def calculate_dynamic_thresholds(results: List[BenchmarkResult]) -> List[float]:
    """Calculate dynamic thresholds based on the distribution of ratios."""

    fastest_time = min(r.avg() for r in results)
    ratios = sorted([r.avg() / fastest_time for r in results])

    thresholds = [
        1.0,
        percentile(ratios, 25),
        percentile(ratios, 40),
        percentile(ratios, 55),
        percentile(ratios, 70),
        percentile(ratios, 80),
        percentile(ratios, 90),
        percentile(ratios, 95),
    ]
    return thresholds


def get_ratio_color(ratio: float, thresholds: List[float]) -> str:
    """Return color based on ratio value using dynamic thresholds."""

    colors = [
        Fore.GREEN,
        Fore.LIGHTGREEN_EX,
        Fore.CYAN,
        Fore.LIGHTCYAN_EX,
        Fore.BLUE,
        Fore.LIGHTBLUE_EX,
        Fore.MAGENTA,
        Fore.LIGHTMAGENTA_EX,
        Fore.RED,
    ]

    for threshold, color in zip(thresholds, colors):
        if ratio <= threshold:
            return color

    return colors[-1]


def print_daily_overview(results: List[BenchmarkResult]) -> None:
    """Print the daily overview table."""
    click.echo(f"\n{Fore.CYAN}📊 Daily Overview{Style.RESET_ALL}")

    thresholds = calculate_dynamic_thresholds(results)

    header = (
        f"| {'Day':>4} | {'Part':>6} | {'Time (avg)':>15} | {'p50':>15} | {'p75':>15} "
        f"| {'p99':>15} | {'Ratio':>8} |"
    )
    separator = (
        f"|{'─' * 6}|{'─' * 8}|{'─' * 17}|{'─' * 17}|{'─' * 17}|{'─' * 17}|{'─' * 10}|"
    )

    click.echo(f"\n{Fore.WHITE}{header}{Style.RESET_ALL}")
    click.echo(f"{Fore.LIGHTBLACK_EX}{separator}{Style.RESET_ALL}")

    fastest_time = min(r.avg() for r in results)
    by_day = {}
    for r in results:
        by_day.setdefault(r.day, []).append(r)

    prev_day = None
    for day in sorted(by_day.keys()):
        day_results = sorted(by_day[day], key=lambda x: x.avg())

        if prev_day is not None:
            click.echo(f"{Fore.LIGHTBLACK_EX}{separator}{Style.RESET_ALL}")

        prev_day = day

        for r in day_results:
            ratio = r.avg() / fastest_time
            ratio_text = f"{ratio:.1f}x"

            color = get_ratio_color(ratio, thresholds)
            line = (
                f"| {r.day:>4} | {r.part:>6} | {format_time(r.avg()):>15} "
                f"| {format_time(r.p(0.50)):>15} | {format_time(r.p(0.75)):>15} "
                f"| {format_time(r.p(0.99)):>15} | {ratio_text:>8} |"
            )
            click.echo(f"{color}{line}{Style.RESET_ALL}")


def print_year_summary(year: int, results: List[BenchmarkResult]) -> None:
    """Print the complete year summary."""
    separator = "─" * 100

    click.echo(f"\n{Fore.YELLOW}Year {year} Summary{Style.RESET_ALL}")
    click.echo(f"{Fore.LIGHTBLACK_EX}{separator}{Style.RESET_ALL}\n")

    print_performance_overview(results)
    print_fastest_slowest(results)
    print_daily_overview(results)


def print_overall_summary(all_results: List[BenchmarkResult]) -> None:
    """Print the complete summary across all years."""
    separator = "─" * 100

    click.echo(f"\n{Fore.YELLOW}Overall Summary{Style.RESET_ALL}")
    click.echo(f"{Fore.LIGHTBLACK_EX}{separator}{Style.RESET_ALL}\n")

    total_time = sum(r.avg() for r in all_results)
    total_solutions = len(all_results)
    years_count = len(set(r.year for r in all_results))

    click.echo(f"{Fore.CYAN}🏃 Performance Overview{Style.RESET_ALL}")
    click.echo(f"Total years: {years_count}")
    click.echo(f"Total solutions: {total_solutions}")
    click.echo(f"Total execution time: {format_time(total_time)}")
    click.echo(f"Average per puzzle: {format_time(total_time / total_solutions)}\n")

    click.echo(f"{Fore.CYAN}📊 Year by Year Overview{Style.RESET_ALL}")
    by_year = {}
    for r in all_results:
        by_year.setdefault(r.year, []).append(r)

    header = (
        f"| {'Year':>4} | {'Solutions':>9} | {'Total Time':>15} | {'Avg Time':>15} | "
        f"{'Fastest':>20} | {'Slowest':>20} |"
    )
    sep = f"|{'─' * 6}|{'─' * 11}|{'─' * 17}|{'─' * 17}|{'─' * 22}|{'─' * 22}|"

    click.echo(f"\n{Fore.WHITE}{header}{Style.RESET_ALL}")
    click.echo(f"{Fore.LIGHTBLACK_EX}{sep}{Style.RESET_ALL}")

    for year in sorted(by_year.keys()):
        year_results = by_year[year]
        year_total = sum(r.avg() for r in year_results)
        year_avg = year_total / len(year_results)

        fastest = min(year_results, key=lambda x: x.avg())
        slowest = max(year_results, key=lambda x: x.avg())

        fastest_str = f"Day {fastest.day} {fastest.part}"
        slowest_str = f"Day {slowest.day} {slowest.part}"

        line = (
            f"| {year:>4} | {len(year_results):>9} | {format_time(year_total):>15} | "
            f"{format_time(year_avg):>15} | {fastest_str:>20} | {slowest_str:>20} |"
        )
        click.echo(f"{Fore.WHITE}{line}{Style.RESET_ALL}")

    click.echo(f"\n{Fore.GREEN}⚡ Top 5 Fastest Solutions{Style.RESET_ALL}")
    for r in sorted(all_results, key=lambda x: x.avg())[:5]:
        click.echo(
            f"Year {r.year} Day {r.day} {r.part}: "
            f"{format_time(r.avg())}/iter{Style.RESET_ALL}"
        )

    click.echo(f"\n{Fore.RED}🐌 Top 5 Slowest Solutions{Style.RESET_ALL}")
    for r in sorted(all_results, key=lambda x: x.avg(), reverse=True)[:5]:
        click.echo(
            f"Year {r.year} Day {r.day} {r.part}: "
            f"{format_time(r.avg())}/iter{Style.RESET_ALL}"
        )

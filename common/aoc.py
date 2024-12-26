import os
import re
import urllib.request

from colorama import Fore, Style
from html2text import HTML2Text
from pyquery import PyQuery as pq

from common.format import rgb_to_ansi


def _headers() -> dict:
    return {
        "Cookie": f"session={os.getenv('AOC_SESSION')}",
        "User-Agent": "contact@xhyrom.dev (Jozef Steinhübl) | github.com/xhyrom/aoc",
    }


def fetch_user_input(year: int, day: int) -> str:
    """Fetches the user input for the given year and day"""

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    request = urllib.request.Request(url, headers=_headers())
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    return data


def fetch_example(year: int, day: int, num: int) -> str:
    """Fetches the example for the given year and day"""

    url = f"https://adventofcode.com/{year}/day/{day}"
    request = urllib.request.Request(url, headers=_headers())
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    d = pq(data)
    examples = d("pre > code")

    if len(examples) <= num - 1:
        raise ValueError(f"Eample {num} not found!")

    return examples[num - 1].text


def fetch_calendar(year: int) -> str:
    """Fetches the calendar for the given year"""

    url = f"https://adventofcode.com/{year}"
    request = urllib.request.Request(url, headers=_headers())
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    d = pq(data)
    main = d("main")
    if main is None:
        raise ValueError("Calendar not found!")

    main.find("div.calendar-bkg").remove()  # 2015
    main.find("div.calendar-printer").remove()  # 2017
    main.find("pre#spacemug").remove()  # 2018
    main.find("span[style*='position:absolute']").remove()  # 2019
    main.find("span.sunbeam").remove()  # 2019
    main.find("span.lavafall").remove()  # 2023
    main.find("span.islefall").remove()  # 2023
    main.find("span.snowfall").remove()  # 2023
    main.find("span.sandfall").remove()  # 2023
    main.find("span.gearfall").remove()  # 2023
    main.find("span[class^='calendar-'][class$='-path']").remove()  # 2024
    main.find("span[class^='calendar-'][class$='-launcher']").remove()  # 2024
    main.find("span[class^='calendar-'][class$='-snowfall']").remove()  # 2024

    calendar = main.html()
    if calendar is None or not isinstance(calendar, str):
        raise ValueError("Calendar not found!")

    calendar = __colorize_calendar(calendar)
    text_maker = HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    text_maker.ignore_emphasis = True

    text = text_maker.handle(calendar)

    lines = text.splitlines()
    lines = [line for line in lines if line.strip()]
    if lines:
        min_padding = min(
            len(line) - len(line.lstrip()) for line in lines if line.strip()
        )
        lines = [line[min_padding:] for line in lines]

    return "\n".join(lines)


def __colorize_calendar(html: str) -> str:
    pattern = re.compile(
        r".calendar ?.(calendar-color-[^ ]+|a.calendar-verycomplete .calendar-ornament\d+) \{ color:\s?#([0-9a-f]{6})"
    )
    matches = pattern.finditer(html)

    colors = {}
    for match in matches:
        class_name, rgb = match.groups()
        class_name = class_name.split(".")[-1].strip()

        r, g, b = int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16)
        colors[class_name] = rgb_to_ansi(r, g, b)

    special_classes = {
        "calendar-mark-complete": f"{Fore.YELLOW}{Style.BRIGHT}",
        "calendar-mark-verycomplete": f"{Fore.YELLOW}{Style.BRIGHT}",
    }

    def replace_span(match):
        class_name = match.group(1)
        text = match.group(2)
        color = colors.get(class_name, special_classes.get(class_name))
        if color:
            return f'<span class="{class_name}">{color}{text}{Style.RESET_ALL}</span>'
        else:
            return match.group(0)

    span_pattern = re.compile(r'<span class="([^"]+)">([^<]*)</span>')
    html = span_pattern.sub(replace_span, html)

    return html

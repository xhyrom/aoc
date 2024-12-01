import os
import urllib.request

from pyquery import PyQuery as pq


def fetch_user_input(year: int, day: int) -> str:
    """Fetches the user input for the given year and day"""

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {"Cookie": f"session={os.getenv('AOC_SESSION')}"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    return data


def fetch_example(year: int, day: int, num: int) -> str:
    """ "Fetches the example for the given year and day"""

    url = f"https://adventofcode.com/{year}/day/{day}"
    headers = {"Cookie": f"session={os.getenv('AOC_SESSION')}"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    d = pq(data)
    examples = d("pre > code")

    if len(examples) <= num - 1:
        raise ValueError(f"Eample {num} not found!")

    return examples[num - 1].text

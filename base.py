import datetime
import urllib.request
import os
from environs import Env
from colorama import Fore, Style


def download_input(env: Env, year: int, day: int) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {"Cookie": f"session={env.str('AOC_SESSION')}"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")
    with open(f"./{year}/{day}/input.txt", "w") as file:
        file.write(data)


def setup(year: int, day: int) -> None:
    os.makedirs(f"./{year}/{day}", exist_ok=True)


# Run this to setup new day
if __name__ == "__main__":
    env = Env()
    env.read_env()

    current_year = datetime.datetime.now().year
    current_day = datetime.datetime.now().day

    setup(current_year, current_day)
    download_input(env, current_year, current_day)

    print(f"{Fore.GREEN}{'*' * 30}")
    print(
        f"{Fore.GREEN}🎄 Advent of Code {current_year} - Day {current_day} {Style.RESET_ALL} 
    )
    print(f"{Fore.GREEN}{'*' * 30}")
    print(
        f"{Fore.BLUE}🔍 Look {Style.BRIGHT}{Fore.YELLOW}https://adventofcode.com/{current_year}/day/{current_day}{Style.RESET_ALL} for more info {Style.RESET_ALL} 
    )
    print(
        f"{Fore.RED}Don't forget to check the problem statement and understand it well! {Style.RESET_ALL} 💡
    )
    print(
        f"{Fore.CYAN}If you finish it or if you're stuck, don't forget to check out other solutions on the solution megathread on Reddit: {Style.BRIGHT}{Fore.YELLOW}https://www.reddit.com/r/adventofcode{Style.RESET_ALL}"
    )
    print(f"{Fore.YELLOW}Happy Coding! {Style.RESET_ALL} 👨‍💻")

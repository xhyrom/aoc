from environs import Env
import urllib.request

env = Env()
env.read_env()

headers = {"Cookie": f"session={env.str('AOC_SESSION')}"}
request = urllib.request.Request(
    "https://adventofcode.com/2023/day/25/answer",
    headers=headers,
    method="POST",
    data="level=2&answer=0".encode("ascii"),
)
response = urllib.request.urlopen(request)

data = response.read().decode("utf-8")
print(data)

# Advent of Code

In this repository, you can find all my solutions to the [Advent of Code](http://adventofcode.com/) challenges mostly written in Python.

### 🌟 What is Advent of Code?

[Advent of Code](http://adventofcode.com/) is an annual coding event featuring 25 programming
puzzles, one for each day from December 1st to December 25th. These puzzles can be solved in
any programming language, offering a fun and engaging way to test your skills and learn new
concepts during the holiday season.

### Usage

To use the tools in this repository, follow these steps:

1. Clone the repository
2. Setup a virtual environment and install dependencies

```bash
python -m venv .env
pip install -r requirements.txt
```

3. Create a `.env` file in the root of the repository with your session token

```bash
echo "AOC_SESSION=<your session token>" > .env
```

Replace `<your session token>` with your session token from the [Advent of Code](http://adventofcode.com/) website.

After that, you can use the provided tool to set up the folder and input file for a new day:

```bash
python base.py
```

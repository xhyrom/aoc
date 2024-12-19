from os.path import abspath, dirname
from shutil import which
from subprocess import run

from common.metadata import Metadata
from common.runners.run import Run, SimpleRun
from common.template import Language


def _get_run_command(language: Language) -> str | None:
    commands = language.commands
    if commands is None:
        return None

    for command in commands:
        bin = command.split()[0]
        path = which(bin)
        if path is not None:
            return command.replace(bin, path)

    return None


def _bench_and_run(command: str, path: str) -> list[Run]:
    cwd = dirname(path)

    process = run(command, cwd=cwd, capture_output=True, text=True, shell=True)

    runs = []

    for line in process.stdout.split("\n"):
        if line.startswith("part_"):  # format: part_n (number): result
            part_number = int(line.split("_")[1].split()[0])
            duration = int(line.split("(")[1].split(")")[0])

            result = line.split(":")[1].strip()
            runs.append(
                SimpleRun(
                    f"part {part_number}",
                    path,
                    None if not result or result == "undefined" else result,
                    duration,
                )
            )
        elif len(runs) > 0 and runs[-1].result is not None:
            runs[-1].result += "\n" + line.strip()
            runs[-1].result = runs[-1].result.strip()
        else:
            if line:
                print(line)

    return runs


def run_naive(year: int, day: int, metadata: Metadata) -> list[Run]:
    runs = []

    run_command = _get_run_command(metadata.language)
    if run_command is None:
        raise ValueError(f"Cannot find a suitable command for {metadata.language}")

    for metadata_file in metadata.files:
        path = abspath(f"./{year}/{day:02}/{metadata_file}")

        runs.extend(_bench_and_run(f"{run_command.format(file=path)}", path))

    return runs

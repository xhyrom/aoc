from os.path import abspath, dirname
from shutil import which
from subprocess import run
from time import perf_counter_ns

from common.metadata import Metadata
from common.runners.run import Run
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

    start = perf_counter_ns()
    process = run(command.split(), cwd=cwd, capture_output=True, text=True)
    end = perf_counter_ns()

    runs = []

    for line in process.stdout.split("\n"):
        if line.startswith("part_"):
            part_number = int(line.split("_")[1].split(":")[0])
            result = line.split(":")[1].strip()
            runs.append(
                Run(
                    f"part {part_number}",
                    path,
                    None if result == "undefined" else result,
                    end - start,
                )
            )
        elif len(runs) > 0 and runs[-1].result is not None:
            runs[-1].result += "\n" + line.strip()
            runs[-1].result = runs[-1].result.strip()
        else:
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

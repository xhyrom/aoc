from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location
from os import chdir, getcwd
from os.path import abspath, dirname
from time import perf_counter_ns
from types import ModuleType
from typing import Callable

from common.metadata import Metadata
from common.runners.run import BenchRun, Run, SimpleRun


@contextmanager
def _temporary_cwd(path):
    """Temporarily change the working directory."""
    old_cwd = getcwd()
    try:
        chdir(path)
        yield
    finally:
        chdir(old_cwd)


def _import(year: int, day: int, file: str) -> tuple[ModuleType, str]:
    path = abspath(f"./{year}/{day:02}/{file}")
    directory = dirname(path)

    spec = spec_from_file_location(file, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot find module {path}")

    module = module_from_spec(spec)

    with _temporary_cwd(directory):
        spec.loader.exec_module(module)

    return module, directory


def _bench_and_run(func: Callable, cwd: str) -> SimpleRun:
    with _temporary_cwd(cwd):
        start = perf_counter_ns()
        result = func()
        end = perf_counter_ns()

        return SimpleRun(func.__name__, func.__code__.co_filename, result, end - start)


def _run_file_part(module: ModuleType, cwd: str, fun: str) -> SimpleRun:
    return _bench_and_run(getattr(module, fun), cwd)


def _run_python_module(module: ModuleType, cwd: str, file: str) -> list[Run]:
    runs = []

    called_func = False

    if hasattr(module, "main"):
        runs.append(_run_file_part(module, cwd, "main"))
        called_func = True

    if hasattr(module, "part_1"):
        runs.append(_run_file_part(module, cwd, "part_1"))
        called_func = True

    if hasattr(module, "part_2"):
        runs.append(_run_file_part(module, cwd, "part_2"))
        called_func = True

    if not called_func:
        runs.append(SimpleRun("anonymous", cwd + f"/{file}", None, 0))

    return runs


def _run_python_module_bench(
    year: int, day: int, module: ModuleType, cwd: str, file: str
) -> list[BenchRun]:
    runs: list[BenchRun] = []

    if (
        not hasattr(module, "main")
        and not hasattr(module, "part_1")
        and not hasattr(module, "part_2")
    ):  # backwards compatibility, 2023
        samples = [] * 10

        for i in range(10):
            start_time = perf_counter_ns()
            _import(year, day, file)
            end_time = perf_counter_ns()
            samples.append(end_time - start_time)

        runs.append(
            BenchRun(
                "part_1" if module.__name__ == "first.py" else "part_2",
                cwd + f"/{file}",
                samples,
            )
        )

        return runs

    if hasattr(module, "part_1"):
        samples = [] * 10

        for i in range(10):
            samples.append(_run_file_part(module, cwd, "part_1").time_taken)

        runs.append(BenchRun("part_1", cwd + f"/{file}", samples))

    if hasattr(module, "part_2"):
        samples = [] * 10

        for i in range(10):
            samples.append(_run_file_part(module, cwd, "part_2").time_taken)

        runs.append(BenchRun("part_2", cwd + f"/{file}", samples))

    return runs


def run_python(
    year: int, day: int, metadata: Metadata, benchmark: bool = False
) -> list[Run]:
    runs = []

    for metadata_file in metadata.files:
        module, cwd = _import(year, day, metadata_file)

        if benchmark:
            runs.extend(_run_python_module_bench(year, day, module, cwd, metadata_file))
        else:
            runs.extend(_run_python_module(module, cwd, metadata_file))

    return runs if year != 2023 else runs[::-1]

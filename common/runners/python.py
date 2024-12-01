from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location
from os import chdir, getcwd
from os.path import abspath, dirname
from time import perf_counter_ns
from types import ModuleType
from typing import Callable

from common.metadata import Metadata
from common.runners.run import Run


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


def _bench_and_run(func: Callable, cwd: str) -> Run:
    with _temporary_cwd(cwd):
        start = perf_counter_ns()
        result = func()
        end = perf_counter_ns()

        return Run(func.__name__, func.__code__.co_filename, result, end - start)


def run_python(year: int, day: int, metadata: Metadata) -> list[Run]:
    runs = []

    for metadata_file in metadata.files:
        module, cwd = _import(year, day, metadata_file)
        called_func = False

        if hasattr(module, "main"):
            runs.append(_bench_and_run(module.main, cwd))
            called_func = True

        if hasattr(module, "part_1"):
            runs.append(_bench_and_run(module.part_1, cwd))
            called_func = True

        if hasattr(module, "part_2"):
            runs.append(_bench_and_run(module.part_2, cwd))
            called_func = True

        if not called_func:
            runs.append(Run("anonymous", cwd + f"/{metadata_file}", None, 0))

    return runs

import os
from importlib import import_module
from typing import TypeVar

import yaml

from dockable.types import Context, Handler, LocalContext, Path

from .file_steps import load_file_steps

K = TypeVar("K")
V = TypeVar("V")


def distinct_merge(data: list[dict[K, V]]) -> dict[K, V]:
    return {k: v for x in data for k, v in x.items()}


def common_merge(data: list[dict[K, V]]) -> dict[K, list[V | None]]:
    return {k: [x.get(k) for x in data] for k in set().union(*data)}


def to_abspath(dir_path: Path, path: Path) -> Path:
    return path if os.path.isabs(path) else os.path.abspath(f"{dir_path}/{path}")


def load_module(dep: str) -> tuple[list[str], dict[str, LocalContext]]:
    def load_modules_yaml(path: Path) -> dict:
        if os.path.isfile(path):
            with open(path) as fh:
                return yaml.safe_load(fh)
        else:
            return {}

    def load_fnc_step(step: str) -> Handler:
        mod, fnc = step.split(":")
        mod_ = import_module(f".{mod}", dep)
        return getattr(mod_, fnc)

    def load_inline_text_step(step: dict) -> LocalContext:
        return {step["name"]: (lambda: step["steps"])}

    mod = import_module(dep)
    dir_path = mod.__path__[0]

    def _load(step: dict | str) -> LocalContext:
        if type(step) is dict and all(k in step for k in ("name", "steps")):
            return load_inline_text_step(step)
        elif type(step) is dict and all(type(x) is str for x in step.values()):
            return {k: load_fnc_step(v) for k, v in step.items()}
        elif type(step) is str:
            return load_file_steps(to_abspath(dir_path, step))
        else:
            raise ValueError("unreachable code")

    data = load_modules_yaml(f"{dir_path}/module.yml")
    includes = [load_module(f"{dep}.{x}") for x in data.get("includes", [])]
    includes2 = [x for _, x in includes]
    includes3 = common_merge(includes2)
    includes4 = {k: [x for x in v if x is not None] for k, v in includes3.items()}
    dependencies = data.get("dependencies", []) + [y for x, _ in includes for y in x]
    return dependencies, {
        k: distinct_merge([_load(x) for x in data.get(k, [])] + includes4.get(k, []))
        for k in ["handlers", "meta_handlers"]
    }


def load_modules(deps: list[str]) -> dict[str, Context]:
    data: dict[str, dict] = {}
    queue = [*deps]
    while len(queue) > 0:
        x = queue.pop()
        if x not in data.keys():
            deps, data[x] = load_module(x)
            queue = queue + deps
    return {
        "meta_handlers": {k: v.get("meta_handlers", {}) for k, v in data.items()},
        "handlers": {k: v.get("handlers", {}) for k, v in data.items()},
    }

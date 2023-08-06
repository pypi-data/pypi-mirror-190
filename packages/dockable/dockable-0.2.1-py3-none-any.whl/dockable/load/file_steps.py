import os
from typing import ParamSpec

import yaml
from jinja2 import ChainableUndefined, Template  # type: ignore

from dockable.types import Handler, LocalContext, Path, Step

P = ParamSpec("P")


def load_template_step(data: str, name: str | None = None) -> tuple[str, Handler]:
    rendered = Template(data, undefined=ChainableUndefined).render({"args": [], "kwargs": {}})
    parsed = yaml.safe_load(rendered)
    name = parsed["name"] if "name" in parsed else name
    if name is None:
        raise ValueError("name must be defined if multiple commands are defined in a single file")

    def _load(*args: P.args, **kwargs: P.kwargs) -> list[Step]:
        rendered = Template(data).render({**kwargs, "args": [*args], "kwargs": kwargs})
        parsed = yaml.safe_load(rendered)
        return parsed["steps"]

    return name, _load


def load_text_step(data: str, name: str | None = None) -> tuple[str, Handler]:
    parsed = yaml.safe_load(data)
    name = parsed["name"] if "name" in parsed else name
    if name is None:
        raise ValueError("name must be defined if multiple commands are defined in a single file")
    return name, lambda: parsed["steps"]


def load_file_steps(file: Path) -> LocalContext:
    with open(file) as fh:
        res = fh.read()
        data = res.split("\n---\n")
    # if we have a single element in the file
    # its ok if it doesnt have a name, use
    # the filename instead
    basename = os.path.basename(file).split(".", 1)[0] if len(data) == 1 else None
    load_fnc = load_template_step if file.endswith(".jinja") else load_text_step
    data2 = [load_fnc(x, basename) for x in data]
    return {k: v for k, v in data2}

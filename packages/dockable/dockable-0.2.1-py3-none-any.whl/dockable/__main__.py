import argparse

import yaml

from ._version import __version__
from .load.module import load_modules
from .render.engine import render
from .types import Path


def _main(input_file: Path, output_file: Path) -> None:
    with open(input_file) as fh:
        data = yaml.safe_load(fh)
    ctx = load_modules(data["dependencies"])
    out = render(ctx, data)
    with open(output_file, "w+") as fh:
        fh.write(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("input", type=str, help="path to docker.yml input file")
    parser.add_argument("output", type=str, help="output Dockerfile")
    args = parser.parse_args()
    _main(args.input, args.output)


main()

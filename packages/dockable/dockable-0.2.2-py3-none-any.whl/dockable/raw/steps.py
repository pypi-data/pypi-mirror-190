from typing import ParamSpecArgs


def raw(*args: ParamSpecArgs) -> list[str]:
    return list(*args)


def run(cmds: list[list[str] | str] | str) -> list[str]:
    def optional_join(infix: str, x: list[str] | str) -> str:
        return x if type(x) is str else infix.join(x)

    commands = optional_join(" \\\n  && ", [optional_join(" \\\n    ", x) for x in cmds])
    return [f"RUN {commands}"]

from dockable.types import Context, Step


def render_step(ctx: Context, step: dict, curr: str) -> list[str]:
    def resolve_dep(key: str) -> tuple[str, str]:
        if key.startswith("."):  # relative
            return curr, key[1:]
        elif "." in key:  # absolute
            mod, fnc = key.rsplit(".", 1)
            return mod, fnc
        else:  # default
            return "dockable.raw", key

    data = [(*resolve_dep(k), v) for k, v in step.items()]
    data2 = [(c, ctx[c][fnc](**v) if type(v) is dict else ctx[c][fnc](v)) for c, fnc, v in data]
    data3 = [render_steps(ctx, s, c) for c, s in data2]
    return [y for x in data3 for y in x]


def render_steps(ctx: Context, steps: list[Step], curr: str = "dockable.raw") -> list[str]:
    def _render(x: Step) -> list[str]:
        if type(x) is dict:
            return render_step(ctx, x, curr)
        elif type(x) is str:
            return [x]
        else:
            raise ValueError("unreachable code")

    data = [_render(x) for x in steps]
    return [y for x in data for y in x]

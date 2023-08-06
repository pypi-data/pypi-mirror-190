from dockable.types import Context

from . import internal


def render_steps(ctx: Context, steps: dict) -> list[str]:
    return internal.render_steps(ctx, [{k: v for k, v in steps.items() if k not in ["steps", "name"]}])

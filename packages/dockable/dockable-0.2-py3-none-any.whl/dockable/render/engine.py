from dockable.types import Context

from . import internal, meta


def render_image(ctx: dict[str, Context], data: dict) -> str:
    return "\n".join(
        meta.render_steps(ctx["meta_handlers"], data) + internal.render_steps(ctx["handlers"], data["steps"])
    )


def render(ctx: dict[str, Context], data: dict) -> str:
    return "\n".join([render_image(ctx, x) for x in data["images"]])

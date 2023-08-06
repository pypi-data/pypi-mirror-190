from collections.abc import Callable
from typing import TypeAlias

Path: TypeAlias = str
Step: TypeAlias = dict | str
Handler: TypeAlias = Callable[..., list[Step]]
LocalContext: TypeAlias = dict[str, Handler]
Context: TypeAlias = dict[str, LocalContext]

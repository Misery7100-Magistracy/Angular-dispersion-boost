from .engine import Engine as Eng
from typing import Any, Callable

# ------------------------- #

class Engine(Eng):

    def __init__(self, loadmethod: Callable, fname: str, **kwargs: Any):
        super().__init__(loadmethod, fname, **kwargs)

# ------------------------- #
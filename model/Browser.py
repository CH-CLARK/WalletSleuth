from typing import Callable


class Browser:
    def __init__(self, name: str, dumper: Callable[[str, str], None] = None) -> None:
        self.name = name
        self.dumper = dumper

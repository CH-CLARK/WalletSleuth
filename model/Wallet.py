from typing import Callable
from model.Browser import Browser


class Wallet:
    def __init__(self, name: str, browsers: list[Browser]=None, dumper: Callable[[str, str], None]=None) -> None:
        self.name = name
        self.browsers = [] if browsers is None else browsers
        self.dumper = dumper

    @property
    def has_browsers(self) -> bool:
        return len(self.browsers) > 0

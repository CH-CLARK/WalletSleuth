import math
from pathlib import Path


class Logger:
    def __init__(self, path: Path):
        self.path = path
    
    def write(self, message: str) -> None:
        with open(self.path, "a") as lf:
            lf.write(message + "\n")
    
    def section_divide(self, title: str) -> None:
        is_even = len(title) % 2 == 0
        multiplier = math.floor(((80 - len(title)) / 2) - 1)

        heading = "-" * 80 + "\n"
        heading = heading + f"{'-' * multiplier}"
        heading = heading + f" {title} "
        heading = heading + f"{'-' * multiplier if is_even else '-' * (multiplier + 1)}\n"
        heading = heading + "-" * 80 + "\n"
        
        self.write(heading)
    
    def read(self) -> str:
        data = ""
        with open(self.path, "r") as lf:
            data = lf.read()
        
        return data

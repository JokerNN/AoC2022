from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

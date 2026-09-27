import math


class Vector2:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = x
        self.y: float = y

    def copy(self) -> Vector2:
        return Vector2(self.x, self.y)

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vector2:
        return Vector2(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)
    
    def clamp(self, lower: Vector2, upper: Vector2):
        return Vector2(max(min(self.x, upper.x), lower.x), max(min(self.y, upper.y), lower.y))

    @property
    def sqrmagnitude(self) -> float:
        return self.x**2 + self.y**2

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.sqrmagnitude)

    def normalised(self) -> Vector2:
        length: float = self.magnitude

        if length == 0:
            return Vector2(0.0, 0.0)

        return Vector2(self.x / length, self.y / length)
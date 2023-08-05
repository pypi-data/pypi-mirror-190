import attr


@attr.s(auto_attribs=True, frozen=True)
class Point:
    """
    A point in 2D space."""

    x: float
    y: float

    def get_x(self) -> float:
        """Get the x coordinate of the point."""
        return self.x

    def get_y(self) -> float:
        """Get the y coordinate of the point."""
        return self.y

    def __add__(self, other: "Point") -> "Point":

        if not isinstance(other, Point):
            raise TypeError(
                "unsupported operand type(s) for +: "
                + f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            raise TypeError(
                "unsupported operand type(s) for -: "
                + f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Point":
        if not isinstance(other, (int, float)):
            raise TypeError(
                "unsupported operand type(s) for *: "
                + f"'{type(self).__name__}' and '{type(other).__name__}'"
            )
        return Point(self.x * other, self.y * other)

    def __rmul__(self, scalar: float) -> "Point":
        return self.__mul__(scalar)

    def __truediv__(self, other: float) -> "Point":
        if not isinstance(other, (int, float)):
            raise TypeError(
                "unsupported operand type(s) for /: "
                + f"'{type(self).__name__}' and '{type(other).__name__}'"
            )
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed")

        return Point(self.x / other, self.y / other)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

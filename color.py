class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def __str__(self):
        return f"#{self.r:02x}{ self.g:02x}{self.b:02x}"

    def __eq__(self, other):
        if isinstance(other, Color):
            return (
                self.r == other.r and
                self.g == other.g and 
                self.b == other.b
            )
        else:
            raise TypeError()

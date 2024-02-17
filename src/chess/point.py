class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash(self.x)+hash(self.y)
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x+other.x, self.y+other.y)
        elif isinstance(other, int):
            return Point(self.x+other, self.y+other)
        elif isinstance(other, tuple):
            return Point(self.x+other[0], self.y+other[1])
        elif isinstance(other, list):
            return Point(self.x+other[0], self.y+other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __iadd__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        elif isinstance(other, int):
            self.x += other
            self.y += other
            return self
        elif isinstance(other, tuple):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x-other.x, self.y-other.y)
        elif isinstance(other, int):
            return Point(self.x-other, self.y-other)
        elif isinstance(other, tuple):
            return Point(self.x-other[0], self.y-other[1])
        elif isinstance(other, list):
            return Point(self.x-other[0], self.y-other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __isub__(self, other):
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            return self
        elif isinstance(other, int):
            self.x -= other
            self.y -= other
            return self
        elif isinstance(other, tuple):
            self.x -= other[0]
            self.y -= other[1]
            return self
        elif isinstance(other, list):
            self.x -= other[0]
            self.y -= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x*other.x, self.y*other.y)
        elif isinstance(other, int):
            return Point(self.x*other, self.y*other)
        elif isinstance(other, tuple):
            return Point(self.x*other[0], self.y*other[1])
        elif isinstance(other, list):
            return Point(self.x*other[0], self.y*other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __imul__(self, other):
        if isinstance(other, Point):
            self.x *= other.x
            self.y *= other.y
            return self
        elif isinstance(other, int):
            self.x *= other
            self.y *= other
            return self
        elif isinstance(other, tuple):
            self.x *= other[0]
            self.y *= other[1]
            return self
        elif isinstance(other, list):
            self.x *= other[0]
            self.y *= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __truediv__(self, other):
        if isinstance(other, Point):
            return Point(self.x/other.x, self.y/other.y)
        elif isinstance(other, int):
            return Point(self.x/other, self.y/other)
        elif isinstance(other, tuple):
            return Point(self.x/other[0], self.y/other[1])
        elif isinstance(other, list):
            return Point(self.x/other[0], self.y/other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __itruediv__(self, other):
        if isinstance(other, Point):
            self.x /= other.x
            self.y /= other.y
            return self
        elif isinstance(other, int):
            self.x /= other
            self.y /= other
            return self
        elif isinstance(other, tuple):
            self.x /= other[0]
            self.y /= other[1]
            return self
        elif isinstance(other, list):
            self.x /= other[0]
            self.y /= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __floordiv__(self, other):
        if isinstance(other, Point):
            return Point(self.x//other.x, self.y//other.y)
        elif isinstance(other, int):
            return Point(self.x//other, self.y//other)
        elif isinstance(other, tuple):
            return Point(self.x//other[0], self.y//other[1])
        elif isinstance(other, list):
            return Point(self.x//other[0], self.y//other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __ifloordiv__(self, other):
        if isinstance(other, Point):
            self.x //= other.x
            self.y //= other.y
            return self
        elif isinstance(other, int):
            self.x //= other
            self.y //= other
            return self
        elif isinstance(other, tuple):
            self.x //= other[0]
            self.y //= other[1]
            return self
        elif isinstance(other, list):
            self.x //= other[0]
            self.y //= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __mod__(self, other):
        if isinstance(other, Point):
            return Point(self.x%other.x, self.y%other.y)
        elif isinstance(other, int):
            return Point(self.x%other, self.y%other)
        elif isinstance(other, tuple):
            return Point(self.x%other[0], self.y%other[1])
        elif isinstance(other, list):
            return Point(self.x%other[0], self.y%other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __imod__(self, other):
        if isinstance(other, Point):
            self.x %= other.x
            self.y %= other.y
            return self
        elif isinstance(other, int):
            self.x %= other
            self.y %= other
            return self
        elif isinstance(other, tuple):
            self.x %= other[0]
            self.y %= other[1]
            return self
        elif isinstance(other, list):
            self.x %= other[0]
            self.y %= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __pow__(self, other):
        if isinstance(other, Point):
            return Point(self.x**other.x, self.y**other.y)
        elif isinstance(other, int):
            return Point(self.x**other, self.y**other)
        elif isinstance(other, tuple):
            return Point(self.x**other[0], self.y**other[1])
        elif isinstance(other, list):
            return Point(self.x**other[0], self.y**other[1])
        else:
            raise ValueError("Invalid operand")
    
    def __ipow__(self, other):
        if isinstance(other, Point):
            self.x **= other.x
            self.y **= other.y
            return self
        elif isinstance(other, int):
            self.x **= other
            self.y **= other
            return self
        elif isinstance(other, tuple):
            self.x **= other[0]
            self.y **= other[1]
            return self
        elif isinstance(other, list):
            self.x **= other[0]
            self.y **= other[1]
            return self
        else:
            raise ValueError("Invalid operand")
    
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def __pos__(self):
        return Point(self.x, self.y)
    
    def __abs__(self):
        return Point(abs(self.x), abs(self.y))
    
    def copy(self):
        return Point(self.x, self.y)
class Cell():
    def __init__(self, x: int, y: int):
        self.__x: int = x
        self.__y: int = y
        self.visited: bool = False
        self.Left: bool = False
        self.Right: bool = False
        self.Top: bool = False
        self.Bottom: bool = False


class Pair():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Maze():
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

        cell = Cell(x = 0, y = 0)
        self.cells = [[cell] * width for i in range(height)]
        for i in range(0, height):
            for j in range(0, width):
                cell = Cell(x = j, y = i)
                self.cells[i][j] = cell
                self.cells[i][j] = cell

    def GetWidth(self):
        return self.__width

    def GetHeight(self):
        return self.__height


if __name__ == "__main__":
    maze = Maze(width=5, height=5)



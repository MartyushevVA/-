class Grid():
    def __init__(self, length, width, cells):
        if (length == int(length) and width == int(width) and cells == list(cells)):
        	self.length = length
            self.width = width
            self.cells = cells
    def checkingCell(self, y, x):
        if self.cells[y][x].isalive:
            if (self.cells[y-1][x-1] + self.cells[y-1][x] + self.cells[y-1][x+1] + self.cells[y][x+1] + self.cells[y+1][x+1]\
                    + self.cells[y+1][x] + self.cells[y+1][x-1] + self.cells[y+1][x] not in laws.survival):
                self.cells[y][x] = 0
        else:
            if (self.cells[y-1][x-1] + self.cells[y-1][x] + self.cells[y-1][x+1] + self.cells[y][x+1] + self.cells[y+1][x+1]\
                    + self.cells[y+1][x] + self.cells[y+1][x-1] + self.cells[y+1][x] in laws.birth):
                self.cells[y][x] = 1


class Cell():
    def __init__(self, isalive):
        self.isalive = isalive


class rules():
    def __init__(self, b, s):
        self.birth = b
        self.survival = s

laws = rules(int(input("Введите количество клеток, для зарождения новой: ")), int(input("Введите количество клеток, для выживания: ")))













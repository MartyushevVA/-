"""""
class Grid():
    def __init__(self, length, width, cells):
        if (length == int(length) and width == int(width) and cells == list(cells)):
            self.length = length
            self.width = width
            self.cells = cells
    def progressingCell(self, y, x):
        if self.cells[y][x].is_alive:
            if (self.cells[y-1][x-1] + self.cells[y-1][x] + self.cells[y-1][x+1] + self.cells[y][x+1] + self.cells[y+1][x+1]\
                    + self.cells[y+1][x] + self.cells[y+1][x-1] + self.cells[y+1][x] not in laws.survive):
                self.cells[y][x] = 0
        else:
            if (self.cells[y-1][x-1] + self.cells[y-1][x] + self.cells[y-1][x+1] + self.cells[y][x+1] + self.cells[y+1][x+1]\
                    + self.cells[y+1][x] + self.cells[y+1][x-1] + self.cells[y+1][x] in laws.birth):
                self.cells[y][x] = 1
"""""


class Grid():
    def __init__(self, length, width, cells):
        if length == int(length) and width == int(width) and cells == list(cells):
            self.length = length
            self.width = width
            self.cells = cells

    def upgradeGrid(self):
        temp = [[0] * self.length] * self.width
        for y in range(self.width):
            for x in range(self.length):
                if self.cells[y][x].is_alive:
                    if (self.cells[y - 1][x - 1] + self.cells[y - 1][x] + self.cells[y - 1][x + 1] + self.cells[y][
                        x + 1] + self.cells[y + 1][x + 1]
                            + self.cells[y + 1][x] + self.cells[y + 1][x - 1] + self.cells[y + 1][
                                x] not in laws.survive):
                        temp[y][x] = 0
                else:
                    if (self.cells[y - 1][x - 1] + self.cells[y - 1][x] + self.cells[y - 1][x + 1] + self.cells[y][
                        x + 1] + self.cells[y + 1][x + 1]
                            + self.cells[y + 1][x] + self.cells[y + 1][x - 1] + self.cells[y + 1][x] in laws.birth):
                        temp[y][x] = 1
        for y in range(self.width):
            for x in range(self.length):
                self.cells[y][x] = temp[y][x]


class Cell():
    def __init__(self, is_alive):
        self.is_alive = is_alive


class rules():
    def __init__(self, birth, survive):
        self.birth = birth
        self.survive = survive


VERTICAL = 1000
HORIZON = 1000
cells = [[0] * VERTICAL] * HORIZON


for i in range(VERTICAL):
    for j in range(HORIZON):
        cells[i][j] = Cell(0)

"""""
Тут должен быть цикл типа while, в котором вызывается Grid.upgradeGrid(HORIZON, VERTICAL, cells)
"""""


laws = rules(int(input("Введите количество клеток, для зарождения новой: ")),
             int(input("Введите количество клеток, для выживания: ")))

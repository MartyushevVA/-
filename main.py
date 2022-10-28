import random


class Grid:
    W_S = 1000
    C_S = 20
    SIZE = W_S // C_S
    cells: dict
    temp: dict
    RULE = '3/2,3'

    def __init__(self):
        self.cells = {j + self.SIZE * i: Cell(i, j) for i in range(self.SIZE) for j in range(self.SIZE)}

    def random_stats(self):
        self.clean_cells()
        for i in range(len(self.cells) // 2):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = True
        self.update_neighbors()

    def update_neighbors(self):
        self.temp = self.cells
        for curr_cell in self.cells.keys():
            count = 0
            for i in range(self.cells[curr_cell].y - 1, self.cells[curr_cell].y + 2):
                for j in range(self.cells[curr_cell].x - 1, self.cells[curr_cell].x + 2):
                    if (i == self.cells[curr_cell].y) and (j == self.cells[curr_cell].x):
                        pass
                    else:
                        if i < 0:
                            i = self.SIZE - 1
                        elif i > self.SIZE:
                            i = 0
                        if j < 0:
                            j = self.SIZE - 1
                        elif j > self.SIZE:
                            j = 0
                        curr_id = j + self.SIZE * i
                        try:
                            if self.cells[curr_id].status:
                                count += 1
                        except:
                            pass
            self.temp[curr_cell].neighbors_count = count
        self.cells = self.temp

    def update_cells(self):
        b = self.RULE.split('/')[0].split(',')
        s = self.RULE.split('/')[1].split(',')
        for key, item in self.cells.items():
            if self.cells[key].status:
                if not (str(item.neighbors_count) in s):
                    self.cells[key].status = False
            else:
                if str(item.neighbors_count) in b:
                    self.cells[key].status = True

    def clean_cells(self):
        self.cells = {j + self.SIZE * i: Cell(i, j) for i in range(self.SIZE) for j in range(self.SIZE)}


class Cell:
    y: int
    x: int
    status: bool
    neighbors_count: int

    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.status = False
        self.neighbors_count = 0


class Rules:
    birth: int
    survive: int
    rule: str

    def __init__(self, birth, survive):
        b = ''
        s = ''
        for i in range(len(str(birth))):
            if i > 0:
                b = b + ',' + str(birth)[i]
            else:
                b = str(birth)[i]
        for i in range(len(str(survive))):
            if i > 0:
                s = s + ',' + str(survive)[i]
            else:
                s = str(survive)[i]
        self.rule = b + '/' + s


laws = Rules(int(input('Введите правило появления клеток: ')),
             int(input("Введите правило выживания клеток: ")))

print(laws.rule)
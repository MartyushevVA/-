import pygame
import random
import sys

W_S = 1000
COLORS = [(40, 40, 40), (255, 100, 135)]

with open('config.txt', 'r', encoding='cp1251') as f:
    RANDOM = f.readline()
    RULE = str(f.readline())[:-1].replace('B', '').replace('S', '')
    NUMHUNTERS = int(f.readline())
    NUMVICTIMS = int(f.readline())
    TIMEHUNTERS = int(f.readline())
    TIMEVICTIMS = int(f.readline())
    RADHUNTER = int(f.readline())
    RADVICTIMS = int(f.readline())
    HUNGRY = int(f.readline())
    DELAY = int(f.readline())
    C_S = int(f.readline())


class Window:
    W_S = W_S
    C_S = C_S

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.W_S, self.W_S))

    def draw_cells(self, cells):
        for i in range(len(cells)):
            if cells[i].status:
                col = COLORS[cells[i].status]
                pygame.draw.rect(self.surface, col,
                                 (cells[i].x * self.C_S, cells[i].y * self.C_S, self.C_S, self.C_S))

    def check_events(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    return ['Start/Stop']
            elif i.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // self.C_S, pos[1] // self.C_S)
                return ['Changing', pos]
        return ['']


class Cell:
    x: int
    y: int
    status: bool
    neighbors_count: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = False
        self.neighbors_count = 0


class CellularAutomaton:
    W_S = W_S
    C_S = C_S
    WIDTH = W_S // C_S
    RULE = RULE
    RANDOM = RANDOM
    cells: dict

    def __init__(self):
        self.cells = {j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        if "True" in RANDOM:
            self.random_stats()

    def random_stats(self):
        for i in range(len(self.cells) // 2):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = True
        self.update_neighbors()

    def update_neighbors(self):
        for curr_cell in self.cells.keys():
            count = 0
            for i in range(self.cells[curr_cell].x - 1, self.cells[curr_cell].x + 2):
                for j in range(self.cells[curr_cell].y - 1, self.cells[curr_cell].y + 2):
                    if (i == self.cells[curr_cell].x) and (j == self.cells[curr_cell].y):
                        pass
                    else:
                        if i < 0:
                            i = self.WIDTH - 1
                        elif i > self.WIDTH:
                            i = 0
                        if j < 0:
                            j = self.WIDTH - 1
                        elif j > self.WIDTH:
                            j = 0
                        curr_id = j + self.WIDTH * i
                        try:
                            if self.cells[curr_id].status:
                                count += 1
                        except:
                            pass
            self.cells[curr_cell].neighbors_count = count

    def update_cells(self):
        RULE_sections = self.RULE.split('/')
        b = RULE_sections[0]
        s = RULE_sections[1]
        for key, item in self.cells.items():
            if self.cells[key].status:
                if not str(item.neighbors_count) in str(s):
                    self.cells[key].status = False
            else:
                if str(item.neighbors_count) in str(b):
                    self.cells[key].status = True


def main():
    PLAY = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            Automaton.update_cells()
            Automaton.update_neighbors()
        pygame.display.update()
        Game.surface.fill((40, 40, 40))
        Game.draw_cells(Automaton.cells)
        result = Game.check_events()
        if result[0] == 'Start/Stop':
            PLAY = not PLAY
        elif result[0] == 'Changing':
            if not Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status == 0:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = 0
            else:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = 1
            Automaton.update_neighbors()
        pygame.time.wait(DELAY)


if __name__ == "__main__":
    main()

import pygame
import random
import sys

W_S = 1000
C_S = 10
RANDOM = 1


class Window:
    W_S = W_S
    C_S = C_S

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.W_S, self.W_S))

    def draw_cells(self, cells):
        for i in range(len(cells)):
            if cells[i].status:
                pygame.draw.rect(self.surface, (255, 100, 135),
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

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = False


class CellularAutomaton:
    W_S = W_S
    C_S = C_S
    WIDTH = W_S // C_S
    cells: dict

    def __init__(self):
        self.cells = {j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        if RANDOM:
            self.random_stats()

    def random_stats(self):
        for i in range(len(self.cells) // 8):
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

    def update_cells(self, ITER):
        if ITER == 0:
            i = 0
            temp = 0
            N = W_S / C_S
            border = int(N / 2)
            while i < (N ** 2 - N - 1):
                for j in range(border):
                    rand = random.randint(0, 2)
                    if rand == 0:
                        temp = self.cells[i + N].status
                        self.cells[i + N].status = self.cells[i].status
                        self.cells[i].status = self.cells[i + 1].status
                        self.cells[i + 1].status = self.cells[i + N + 1].status
                        self.cells[i + N + 1].status = temp
                    if rand == 1:
                        temp = self.cells[i + N + 1].status
                        self.cells[i + N + 1].status = self.cells[i + 1].status
                        self.cells[i + 1].status = self.cells[i].status
                        self.cells[i].status = self.cells[i + N].status
                        self.cells[i + N].status = temp
                    temp = 0
                    i += 2
                i += N


def main():
    PLAY = 0
    ITER = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            Automaton.update_cells(ITER)
        pygame.display.update()
        Game.surface.fill((40, 40, 40))
        Game.draw_cells(Automaton.cells)
        result = Game.check_events()
        if result[0] == 'Start/Stop':
            PLAY = not PLAY
        elif result[0] == 'Changing':
            if not Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = True
            else:
                Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = False
            Automaton.update_neighbors()
        ITER = 1 - ITER


if __name__ == "__main__":
    main()

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

    def __init__(self, y, x):
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
        for i in range(len(self.cells) // 64):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = True


    def update_cells(self, ITER):
        temp = 0
        N = W_S / C_S
        if ITER == 0:
            i = 0
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

        if ITER == 0:
            i = N + 1
            border = int(N / 2) - 1
            while i < (N ** 2 - 2 * N - 2):
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
                i += N + 2


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
        pygame.time.wait(10)


if __name__ == "__main__":
    main()

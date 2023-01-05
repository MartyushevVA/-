import pygame
import random
import sys

W_S = 1000
C_S = 10
COLORS = [(40, 40, 40), (37, 213, 0), (246, 0, 24)]
NUMHUNTERS = 100
NUMVICTIMS = 500
TIMEHUNTERS = 10
TIMEVICTIMS = 10
HUNGRY = 100
RADHUNTER = 20
RADVICTIMS = 5


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
            # elif i.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     pos = (pos[0] // self.C_S, pos[1] // self.C_S)
            #     return ['Changing', pos]
        return ['']


class Cell:
    x: int
    y: int
    status: int
    time_of_reproduction: int
    time_of_hungry: int
    location_of_closest_opponent: int
    close_opp: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0


class CellularAutomaton:
    W_S = W_S
    C_S = C_S
    WIDTH = W_S // C_S
    cells: dict
    hunters: list
    victims: list

    def __init__(self):
        self.cells = {j + self.WIDTH * i: Cell(i, j) for i in range(self.WIDTH) for j in range(self.WIDTH)}
        self.victims = []
        self.hunters = []
        self.random_stats()

    def random_stats(self):
        for i in range(NUMVICTIMS):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = 1
            self.victims.append(random_id)
            self.cells[random_id].time_of_reproduction = TIMEVICTIMS
        for i in range(NUMHUNTERS):
            random_id = random.randint(0, len(self.cells) - 1)
            self.cells[random_id].status = 2
            self.hunters.append(random_id)
            self.cells[random_id].time_of_reproduction = TIMEHUNTERS
            self.cells[random_id].time_of_hungry = HUNGRY
        self.closest_opponent()


    def closest_opponent(self):
        for vic in self.victims:
            minr = 9999
            for hun in self.hunters:
                if pow((pow((abs(self.cells[vic].x - self.cells[hun].x) - 1), 2) + pow((abs(self.cells[vic].y - self.cells[hun].y) - 1), 2)), 0.5) < minr:
                    minr = pow((pow((abs(self.cells[vic].x - self.cells[hun].x) - 1), 2) + pow((abs(self.cells[vic].y - self.cells[hun].y) - 1), 2)), 0.5)
                    self.cells[vic].close_opp = hun
            self.cells[vic].location_of_closest_opponent = minr
        for hun in self.hunters:
            minr = 9999
            for vic in self.victims:
                if pow((pow((abs(self.cells[vic].x - self.cells[hun].x) - 1), 2) + pow((abs(self.cells[vic].y - self.cells[hun].y) - 1), 2)), 0.5) < minr:
                    minr = pow((pow((abs(self.cells[vic].x - self.cells[hun].x) - 1), 2) + pow((abs(self.cells[vic].y - self.cells[hun].y) - 1), 2)), 0.5)
                    self.cells[hun].close_opp = vic
            self.cells[hun].location_of_closest_opponent = minr


    def update_cells(self, time):
        ti = time
        for key, item in self.cells.items():
            napr = random.randint(0, 8)
            if self.cells[key].status == 2:
                if self.cells[key].location_of_closest_opponent <= RADHUNTER:
                    if self.cells[self.cells[key].close_opp].x > self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 7
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 1
                        if self.cells[self.cells[key].close_opp].y == self.cells[key].y:
                            napr = 0
                    if self.cells[self.cells[key].close_opp].x == self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 6
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 2
                    if self.cells[self.cells[key].close_opp].x < self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 5
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 3
                        if self.cells[self.cells[key].close_opp].y == self.cells[key].y:
                            napr = 4
            if self.cells[key].status == 1:
                if self.cells[key].location_of_closest_opponent <= RADVICTIMS:
                    if self.cells[self.cells[key].close_opp].x > self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 3
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 5
                        if self.cells[self.cells[key].close_opp].y == self.cells[key].y:
                            napr = 4
                    if self.cells[self.cells[key].close_opp].x == self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 2
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 6
                    if self.cells[self.cells[key].close_opp].x < self.cells[key].x:
                        if self.cells[self.cells[key].close_opp].y > self.cells[key].y:
                            napr = 1
                        if self.cells[self.cells[key].close_opp].y < self.cells[key].y:
                            napr = 7
                        if self.cells[self.cells[key].close_opp].y == self.cells[key].y:
                            napr = 0
            temp = Cell(-1, -1)
            temp = self.cells[key]
            if napr == 0:
                self.cells[key] = self.cells[key + 1]
                self.cells[key + 1] = temp
            if napr == 1:
                self.cells[key] = self.cells[key - self.WIDTH + 1]
                self.cells[key - self.WIDTH + 1] = temp
            if napr == 2:
                self.cells[key] = self.cells[key - self.WIDTH]
                self.cells[key - self.WIDTH] = temp
            if napr == 3:
                self.cells[key] = self.cells[key - self.WIDTH - 1]
                self.cells[key - self.WIDTH - 1] = temp
            if napr == 4:
                self.cells[key] = self.cells[key - 1]
                self.cells[key - 1] = temp
            if napr == 5:
                self.cells[key] = self.cells[key + self.WIDTH - 1]
                self.cells[key + self.WIDTH - 1] = temp
            if napr == 6:
                self.cells[key] = self.cells[key + self.WIDTH]
                self.cells[key + self.WIDTH] = temp
            if napr == 7:
                self.cells[key] = self.cells[key + self.WIDTH + 1]
                self.cells[key + self.WIDTH + 1] = temp





def main():
    PLAY = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            Automaton.update_cells(pygame.time.get_ticks())
            Automaton.closest_opponent()
        pygame.display.update()
        Game.surface.fill((40, 40, 40))
        Game.draw_cells(Automaton.cells)
        result = Game.check_events()
        if result[0] == 'Start/Stop':
            PLAY = not PLAY
        # elif result[0] == 'Changing':
        #     Automaton.cells[result[1][1] + result[1][0] * Automaton.WIDTH].status = (Automaton.cells[
        #                                                                                  result[1][1] + result[1][
        #                                                                                      0] * Automaton.WIDTH].status + 1) % 3
            Automaton.closest_opponent()
        pygame.time.wait(0)


if __name__ == "__main__":
    main()

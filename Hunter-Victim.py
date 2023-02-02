import pygame
import random
import sys

f = open('config.txt')

W_S = 1000
C_S = int(f.readline())
COLORS = [(40, 40, 40), (37, 213, 0), (246, 0, 24)]
NUMHUNTERS = 100
NUMVICTIMS = 500
TIMEHUNTERS = 100
TIMEVICTIMS = 100
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
    napr: int
    repr: bool
    next_status: int
    next_time_of_reproduction: int
    next_time_of_hungry: int
    next_location_of_closest_opponent: int
    next_close_opp: int
    next_napr: int
    next_repr: bool

    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.status = 0
        self.time_of_reproduction = 0
        self.time_of_hungry = 0
        self.repr = False
        self.napr = 0
        self.next_status = 0
        self.next_time_of_reproduction = 0
        self.next_time_of_hungry = 0
        self.next_repr = False
        self.next_napr = 0


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
        #self.WIDTH, self.WIDTH * (self.WIDTH - 1) - 1
        for i in range(NUMVICTIMS):
            random_id = random.randint(0, self.WIDTH**2 - 1)
            self.cells[random_id].status = 1
            self.victims.append(random_id)
            self.cells[random_id].time_of_reproduction = 0
        for i in range(NUMHUNTERS):
            random_id = random.randint(0, self.WIDTH**2 - 1)
            self.cells[random_id].status = 2
            self.hunters.append(random_id)
            self.cells[random_id].time_of_reproduction = 0
            self.cells[random_id].time_of_hungry = 0

    def update_roles(self):
        self.victims.clear()
        self.hunters.clear()
        for key, item in self.cells.items():
            if item.status == 1:
                self.victims.append(key)
            if item.status == 2:
                self.hunters.append(key)

    def closest_opponent(self):
        for vic in self.victims:
            minr = 1000
            for hun in self.hunters:
                if pow((pow((abs(self.cells[vic].x - self.cells[hun].x)), 2) + pow(
                        (abs(self.cells[vic].y - self.cells[hun].y)), 2)), 0.5) < minr:
                    minr = pow((pow((abs(self.cells[vic].x - self.cells[hun].x)), 2) + pow(
                        (abs(self.cells[vic].y - self.cells[hun].y)), 2)), 0.5)
                    self.cells[vic].close_opp = hun
            self.cells[vic].location_of_closest_opponent = minr
        for hun in self.hunters:
            minr = 1000
            for vic in self.victims:
                if pow((pow((abs(self.cells[vic].x - self.cells[hun].x)), 2) + pow(
                        (abs(self.cells[vic].y - self.cells[hun].y)), 2)), 0.5) < minr:
                    minr = pow((pow((abs(self.cells[vic].x - self.cells[hun].x)), 2) + pow(
                        (abs(self.cells[vic].y - self.cells[hun].y)), 2)), 0.5)
                    self.cells[hun].close_opp = vic
            self.cells[hun].location_of_closest_opponent = minr

    def direction(self):
        masnapr = [1, 1 - self.WIDTH, - self.WIDTH, - self.WIDTH - 1, -1, self.WIDTH - 1, self.WIDTH, self.WIDTH + 1]
        for key, item in self.cells.items():
            if item.status:
                flag = 0
                napr = 0
                if item.status == 2:
                    if item.location_of_closest_opponent <= RADHUNTER:
                        flag = 1
                        if self.cells[item.close_opp].x > item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 7
                            if self.cells[item.close_opp].y < item.y:
                                napr = 1
                            if self.cells[item.close_opp].y == item.y:
                                napr = 0
                        if self.cells[item.close_opp].x == item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 6
                            if self.cells[item.close_opp].y < item.y:
                                napr = 2
                        if self.cells[item.close_opp].x < item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 5
                            if self.cells[item.close_opp].y < item.y:
                                napr = 3
                            if self.cells[item.close_opp].y == item.y:
                                napr = 4
                if item.status == 1:
                    if item.location_of_closest_opponent <= RADVICTIMS:
                        flag = 1
                        if self.cells[item.close_opp].x > item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 3
                            if self.cells[item.close_opp].y < item.y:
                                napr = 5
                            if self.cells[item.close_opp].y == item.y:
                                napr = 4
                        if self.cells[item.close_opp].x == item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 2
                            if self.cells[item.close_opp].y < item.y:
                                napr = 6
                        if self.cells[item.close_opp].x < item.x:
                            if self.cells[item.close_opp].y > item.y:
                                napr = 1
                            if self.cells[item.close_opp].y < item.y:
                                napr = 7
                            if self.cells[item.close_opp].y == item.y:
                                napr = 0
                if flag == 0:
                    if (key + 1) % self.WIDTH == 0:
                        if key // self.WIDTH == 0:
                            napr = random.randint(4, 6)
                        if key // self.WIDTH == self.WIDTH - 1:
                            napr = random.randint(2, 4)
                        else:
                            napr = random.randint(2, 6)
                    if key % self.WIDTH == 0:
                        if key // self.WIDTH == 0:
                            tmr = [0, 6, 7]
                            napr = tmr[random.randint(0, 2)]
                        if key // self.WIDTH == self.WIDTH - 1:
                            napr = random.randint(0, 2)
                        else:
                            tmr = [0, 1, 2, 6, 7]
                            napr = tmr[random.randint(0, 4)]
                    elif key // self.WIDTH == 0:
                        tmr = [0, 4, 5, 6, 7]
                        napr = tmr[random.randint(0, 4)]
                    elif key // self.WIDTH == self.WIDTH - 1:
                        napr = random.randint(0, 4)
                    else:
                        napr = random.randint(0, 7)
                item.napr = masnapr[napr]

    def time_checking(self, time):
        reproduction_massive = [TIMEVICTIMS*100, TIMEHUNTERS*100]
        for key, item in self.cells.items():
            flag = 1
            if item.status:
                if item.status == 2:
                    if time - item.time_of_hungry > HUNGRY*100:
                        item.status = 0
                        flag = 0
                if flag:
                    if time - item.time_of_reproduction >= reproduction_massive[item.status - 1]:
                        item.repr = 1


    def reproduction(self, curr_cell): #без учета партнера
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
                    try:
                        if self.cells[j + self.WIDTH * i].status == 0 and self.cells[j + self.WIDTH * i].next_status == 0:
                            self.cells[j + self.WIDTH * i].next_status = self.cells[curr_cell].next_status
                            self.cells[j + self.WIDTH * i].status = self.cells[curr_cell].next_status
                            self.cells[j + self.WIDTH * i].next_time_of_hungry = pygame.time.get_ticks()
                            self.cells[j + self.WIDTH * i].time_of_hungry = pygame.time.get_ticks()
                            self.cells[j + self.WIDTH * i].next_time_of_reproduction = pygame.time.get_ticks()
                            self.cells[j + self.WIDTH * i].time_of_reproduction = pygame.time.get_ticks()
                            self.cells[j + self.WIDTH * i].next_repr = 0
                            self.cells[j + self.WIDTH * i].repr = 0
                            self.cells[curr_cell].next_repr = 0
                            self.cells[curr_cell].repr = 0
                            return
                    except:
                        pass




    def movement(self):
        for key, item in self.cells.items():
            try:
                if item.status == 1:
                    if self.cells[key + item.napr].next_status == 0:
                        self.cells[key + item.napr].next_status = 1
                        self.cells[key + item.napr].next_time_of_reproduction = item.time_of_reproduction
                        self.cells[key + item.napr].next_time_of_hungry = item.time_of_hungry
                        self.cells[key + item.napr].next_repr = item.repr
                    elif self.cells[key + item.napr].next_status == 1:
                        item.next_status = 1
                        item.next_time_of_reproduction = item.time_of_reproduction
                        item.next_repr = item.repr
                    elif self.cells[key + item.napr].next_status == 2:
                        item.next_status = 1
                        item.next_time_of_reproduction = item.time_of_reproduction
                        item.next_repr = item.repr

                if item.status == 2:
                    if self.cells[key + item.napr].next_status == 0:
                        self.cells[key + item.napr].next_status = 2
                        self.cells[key + item.napr].next_time_of_reproduction = item.time_of_reproduction
                        self.cells[key + item.napr].next_time_of_hungry = item.time_of_hungry
                        self.cells[key + item.napr].next_repr = item.repr
                    elif self.cells[key + item.napr].next_status == 1:
                        self.cells[key + item.napr].next_status = 2
                        self.cells[key + item.napr].status = 0
                        self.cells[key + item.napr].next_time_of_reproduction = item.time_of_reproduction
                        self.cells[key + item.napr].next_time_of_hungry = pygame.time.get_ticks()
                        self.cells[key + item.napr].next_repr = item.repr
                    elif self.cells[key + item.napr].next_status == 2:
                        item.next_status = 2
                        item.next_time_of_reproduction = item.time_of_reproduction
                        item.next_time_of_hungry = item.time_of_hungry
                        item.next_repr = item.repr
            except:
                pass
        for key, item in self.cells.items():
            item.status = item.next_status
            item.time_of_reproduction = item.next_time_of_reproduction
            item.time_of_hungry = item.next_time_of_hungry
            # if item.next_repr:
            #     self.reproduction(key)
            item.next_status = 0



def main():
    PLAY = 0
    Game = Window()
    Automaton = CellularAutomaton()
    while True:
        if PLAY:
            time = pygame.time.get_ticks()
            Automaton.closest_opponent()
            Automaton.direction()
            Automaton.time_checking(time)
            Automaton.movement()
            Automaton.update_roles()
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

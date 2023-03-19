import os
from clouds import Clouds
from utils import *

CELL_TYPES = '🟩🌲🌊🏭🏦🔥'
TREE_BONUS = 100
UPGRADE_PRICE = 500
LIFE_PRICE = 1000


class Map:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(3, 10)
        self.generate_river(10)
        self.generate_river(7)
        self.generate_river(7)
        self.generate_shop()
        self.generate_repair_shop()
        self.clouds = Clouds(w, h)

    def map_print(self, heli):
        print('⬛' * (self.w + 2))
        for ri in range(self.h):
            print('⬛', end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if self.clouds.cells[ri][ci] == 1:
                    print('⬜', end='')
                elif self.clouds.cells[ri][ci] == 2:
                    print('🟨', end='')
                elif heli.x == ri and heli.y == ci:
                    print('🚁', end='')
                elif 0 <= cell < len(CELL_TYPES):
                    print(CELL_TYPES[cell], end='')
            print('⬛', end='')
            print()
        print('⬛' * (self.w + 2))

    def check_bounds(self, x, y):
        if (x < 0) or (y < 0) or (x >= self.h) or (y >= self.w):
            return False
        else:
            return True

    def generate_tree(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        # if self.check_bounds(cx, cy) and self.cells[cx][cy] == 0:
        self.cells[cx][cy] = 1

    def generate_river(self, l):
        rc = rand_cell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2

        while l > 0:
            rc_next = rand_neighbour(rx, ry)
            rx_next, ry_next = rc_next[0], rc_next[1]
            if self.check_bounds(rx_next, ry_next):
                self.cells[rx_next][ry_next] = 2
                rx, ry = rx_next, ry_next
                l -= 1

        self.cells[rx][ry] = 2

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if rand_bool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_shop(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4

    def generate_repair_shop(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_repair_shop()

    def add_fire(self):
        c = rand_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        [self.add_fire() for i in range(5)]

    def process_heli(self, heli):
        c = self.cells[heli.x][heli.y]
        d = self.clouds.cells[heli.x][heli.y]
        if c == 2:
            heli.tank = heli.max_tank
        if c == 5 and heli.tank > 0:
            heli.tank -= 1
            heli.score += TREE_BONUS
            self.cells[heli.x][heli.y] = 1
        if c == 4 and heli.score >= UPGRADE_PRICE:
            heli.score -= UPGRADE_PRICE
            heli.max_tank += 1
        if c == 3 and heli.score >= LIFE_PRICE:
            heli.score -= LIFE_PRICE
            if heli.max_lives < 1000:
                heli.max_lives += 100
                heli.lives = heli.max_lives
                heli.health_dashes = heli.max_lives // 100
            else:
                heli.lives = heli.max_lives
        if d == 2:
            heli.lives -= 2
            if heli.lives == 0:
                os.system('cls')
                print(f'GAME OVER. FINAL SCORE {heli.score}')
                exit(0)

    def export_data(self):
        return {'cells': self.cells, }

    def import_data(self, data):
        self.cells = data['cells']

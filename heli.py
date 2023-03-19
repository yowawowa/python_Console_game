import math

from utils import rand_cell


class Heli:
    def __init__(self, w, h):
        rc = rand_cell(w, h)
        rx, ry = rc[0], rc[1]
        self.x, self.y = rx, ry
        self.w, self.h = w, h
        self.max_tank = 1
        self.tank = 0
        self.score = 0
        self.lives = 300
        self.max_lives = 300
        self.health_dashes = self.max_lives // 100

    def move(self, dx, dy):
        nx, ny = dx + self.x, dy + self.y
        if 0 <= nx < self.h and 0 <= ny < self.w:
            self.x, self.y = nx, ny

    def lives_counter(self):
        dash_convert = int(self.max_lives / self.health_dashes)
        current_dashes = int(self.lives / dash_convert)
        remaining_health = self.health_dashes - current_dashes

        health_display = '🔧' * current_dashes
        remaining_display = ' ' * remaining_health
        percent = str(int((self.lives / self.max_lives) * 100)) + "%"
        return health_display + remaining_display + "|" + percent

    def menu_print(self):
        print(f'🧺 {self.tank}/{self.max_tank} | 💰 {self.score}', sep='')
        print(f'🔧{self.lives_counter()}')

    def export_data(self):
        return {'score': self.score,
                'lives': self.lives,
                'max_lives': self.max_lives,
                'tank': self.tank,
                'max_tank': self.max_tank,
                'x': self.x,
                'y': self.y,
                }

    def import_data(self, data):
        self.x = data['x'] or 0
        self.y = data['y'] or 0
        self.tank = data['tank'] or 0
        self.score = data['score'] or 0
        self.lives = data['lives'] or 100
        self.max_lives = data['max_lives'] or 300



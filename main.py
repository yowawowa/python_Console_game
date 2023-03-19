from clouds import Clouds
from map import Map
from heli import Heli
import json
import time
import os
from pynput import keyboard

TICK_SLEEP = 0.01
TREE_UPDATE = 50
FIRE_UPDATE = 100
CLOUD_UPDATE = 100
MAP_W, MAP_H = 20, 10

MOVES = {
    'w': (-1, 0),
    'a': (0, -1),
    's': (1, 0),
    'd': (0, 1),
}

forest = Map(MAP_W, MAP_H)
heli = Heli(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
tick = 1


def key_input(key):
    global heli, tick, clouds, forest
    c = key.char.lower()
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        heli.move(dx, dy)
    elif c =='f':
        data ={'heli':heli.export_data(),
               'clouds': clouds.export_data(),
               'map' : forest.export_data(),
               'tick': tick,}
        with open('level.json', 'w') as lvl:
          json.dump(data, lvl)
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            heli.import_data(data['heli'])
            tick = data['tick'] or 1
            forest.import_data(data['map'])
            clouds.import_data(data['clouds'])



listener = keyboard.Listener(on_release=key_input)
listener.start()


while True:
    os.system('cls')
    forest.process_heli(heli)
    heli.menu_print()
    forest.map_print(heli)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if tick % TREE_UPDATE == 0:
        forest.generate_tree()
    if tick % FIRE_UPDATE == 0:
        forest.update_fires()
    if tick % CLOUD_UPDATE == 0:
        forest.clouds.update()

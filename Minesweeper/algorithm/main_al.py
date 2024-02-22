import json
import time
from functions import Map
from os import remove

Map = Map()
# last_file = -1


def open_file(n):
    while 1:
        try:
            with open('open_cells.json', 'r') as f:
                data = json.load(f)
            break
        except OSError or json.decoder.JSONDecodeError:
            time.sleep(0.5)
    # return data if n < data['count'] else None
    return data


while not Map.GAME_OVER:
    file = open_file()
    if not file:
        continue

    print('start Map')
    # last_file += 1
    Map.update(file)
    Map.analise()
    Map.send_moves()
    # Map.draw()
    # print()
    time.sleep(1/24)

remove('moves.json')
remove('open_cells.json')
remove('parameters.json')

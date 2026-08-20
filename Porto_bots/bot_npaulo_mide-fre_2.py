# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   bot_npaulo_mide-fre_2.py                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: npaulo <npaulo@student.42porto.com>         +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/08/20 18:03:51 by npaulo             #+#    #+#             #
#   Updated: 2026/08/20 19:01:34 by npaulo            ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

BOT_NAME = "Ctrl+C Bot"
BOT_COLOR = "#f4a261"
MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


def read_op_pos(players):
    for player in players.values():
        if BOT_NAME != player['name']:
            return {'opponent', (player['direction'], player['pos'])}
    return {'opponent', ('NONE', (0, 0))}


def check_visit(width, height, pos, walls, visited):
    x, y = pos
    if ((x, y) not in walls and (x, y) not in visited and 0 <= x < width and 0 <= y < height):
        return False
    return True


def flood_fill(width, height, pos, walls):
    line = [pos]
    visited = {pos}
    while len(line) > 0:
        x, y = line.pop(0)
        for dx, dy in MOVES.values():
            if not check_visit(width, height, (x + dx, y + dy), walls, visited):
                visited.add((x + dx, y + dy))
                line.append((x + dx, y + dy))

    return len(visited)


def count_open_neighbors(pos, walls, width, height):
    x, y = pos
    count = 0
    for dx, dy in MOVES.values():
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
            count += 1
    return count


def get_move(state):
    me = state["players"][state["you"]]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]

    best_move, best_score = None, -1
    for direction, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height) or (nx, ny) in walls:
            continue

        print(read_op_pos(state['players']))
        # my_map = count_open_neighbors(
        #     (nx, ny), walls | {(nx, ny)}, width, height)
        score = flood_fill(width, height, (nx, ny), walls)
        # score = oponent_map - my_map
        if score > best_score:
            best_move, best_score = direction, score

    return best_move or "UP"

BOT_NAME = "BLACKHOLE"
BOT_COLOR = "#ff0404"
MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


def in_bounds(pos, width, height):
    x, y = pos
    return 0 <= x < width and 0 <= y < height

def found_oponent(opo, player, move, walls, width, height, state):
    lista = [
        "UP",
        "DOWN",
        "LEFT",
        "RIGHT"
    ]
    px, py = player
    next_move = move[-1]
    nx, ny = MOVES[next_move]
    value = (nx - px, ny - py)
    invalids = []
    valids = []
    if (in_bounds(value)):
        if (value in walls):
            lista.remove(next_move)
            move = move[0:-1]
        next_move = move[-1]
        for valor in lista:
            x, y = MOVES[valor]
            if not in_bounds((x, y), width, height) or (x, y) in walls:
                invalids.append(valor)
            else:
                valids.append(valor)
    return move + valids




def count_open_neighbors(pos, walls, width, height):
    x, y = pos
    count = 0
    for dx, dy in MOVES.values():
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) in walls:
            count += 1
    return count


def get_move(state):
    me = state["players"][state["you"]]
    enemy_posi = state["players"][1 if state["you"] else 0]["pos"]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]

    best_move, best_score = None, -1
    for direction, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height) or (nx, ny) in walls:
            continue
        score = count_open_neighbors((nx, ny), walls | {(nx, ny)}, width, height)
        if score > best_score:
            if state["turn"] != 100:
                best_move, best_score = direction, score
            else:
                best_move = found_oponent(enemy_posi, direction, best_move, state["walls"], width, height, state["turn"])
                best_score = score

    return best_move or "LEFT"

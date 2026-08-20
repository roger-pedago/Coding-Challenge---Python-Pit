BOT_NAME = "Suboptimal Prime"
BOT_COLOR = "#f900b7"
MOVES = {
    "DOWN": (0, 1),
    "UP": (0, -1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
MOVES2 = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "RIGHT": (1, 0),
    "LEFT": (-1, 0),
    "HA": (0, 0)
}


def get_move(state):
    global moveset

    me = state["players"][state["you"]]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]

    if state["turn"] == 0:
        if y < 10:
            moveset  = MOVES
        else:
            moveset = MOVES2

    if moveset == MOVES:
        if y < 11 and x == 2:
            if 0 <= x < width and 0 <= (y - 1) < height and (x, y - 1) not in walls:
                return "DOWN"
        if y == 10:
            if 0 <= (x + 1) < width and 0 <= y < height and (x + 1,  y) not in walls:
                return "RIGHT"
        for direction, (dx, dy) in moveset.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                return direction
    elif moveset == MOVES2:
        if y > 10 and x == 17:
            if 0 <= x < width and 0 <= (y - 1) < height and (x, y - 1) not in walls:
                return "UP"
        if y == 10:
            if 0 <= (x - 1) < width and 0 <= y < height and (x - 1,  y) not in walls:
                return "LEFT"
        for direction, (dx, dy) in moveset.items():
            if direction == "HA":
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                return direction

    return "UP"

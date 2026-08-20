BOT_NAME = "KamikazeBot"
BOT_COLOR = "#f4a261"
MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

MODE = None
LAST_MOVE = None

def abs(x: int | float) -> int | float:
    return x if x >= 0 else -x

def get_mode(state) -> tuple[str, str]:
    me = state["players"][state["you"]]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]
    if abs(width - 1 - x) >= abs(0 - 1 - x):
        x_mode = "RIGHT"
    else:
        x_mode = "LEFT"
    if abs(height - 1 - y) >= abs(0 - 1 - x):
        y_mode = "DOWN"
    else:
        y_mode = "UP"
    return (x_mode, y_mode)



def count_open_neighbors(pos, walls, width, height):
    x, y = pos
    count = 0
    for dx, dy in MOVES.values():
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
            count += 1

def get_move(state):
    global MODE
    global LAST_MOVE
    if not hasattr(get_move, "passed"):
        MODE = get_mode(state)
        get_move.passed = True
        LAST_MOVE = MODE[0]
        return LAST_MOVE
    me = state["players"][state["you"]]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]
    if LAST_MOVE == MODE[0]:
        LAST_MOVE = MODE[1]
        return LAST_MOVE
    LAST_MOVE = MODE[0]
    return LAST_MOVE

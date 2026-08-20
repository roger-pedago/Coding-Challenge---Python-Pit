from collections import deque

BOT_NAME = "Exterminator"
BOT_COLOR = "#d91515e7"

MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

OPPOSITE = {
    "UP": "DOWN", 
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT"
}


def in_bounds(x, y, width, height):
    return 0 <= x < width and 0 <= y < height


def flood_fill(start, walls, widht, height):
    distances = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in MOVES.values():
            next_cell = (x + dx, y + dy)
            next_x, next_y = (next_cell)
            if not in_bounds(next_x, next_y, widht, height):
                continue
            if next_cell in walls or next_cell in distances:
                continue
    
            distances[next_cell] = distances[(x, y)] + 1
            queue.append(next_cell)
    return distances


def real_space(distances):
    odd_sum = 0
    for x, y in distances:
        if (x + y) % 2 == 1:
            odd_sum += 1
    even_sum = len(distances) - odd_sum
    if odd_sum == even_sum:
        return 2 * odd_sum
    return 2 * min(odd_sum, even_sum) + 1


def territory(my_position, enemy_position, walls, width, height):

    my_reaches = flood_fill(my_position, walls, width, height)

    enemy_reaches = flood_fill(enemy_position, walls | {my_position}, width, height)

    separated = True
    for cell in my_reaches:
        if cell in enemy_reaches:
            separated = False
            break
    if separated:
        return real_space(my_reaches) - real_space(enemy_reaches)

    score = 0
    for cell, my_distance in my_reaches.items():
        enemy_distance = enemy_reaches.get(cell)
        if enemy_distance is None:
            score += 1
        elif my_distance < enemy_distance:
            score += 1
        elif enemy_distance < my_distance:
            score -= 1
    for cell in enemy_reaches:
        if cell not in my_reaches:
            score -= 1
    return score

def find_enemy(state, my_position):
    enemies = []
    for player_id, player in state["players"].items():
        if player_id == state["you"]:
            continue
        if not player["alive"]:
            continue
        enemies.append(player)

    if not enemies:
        return None
    
    def distance_to_me(player):
            player_x, player_y = player["pos"]
            return abs(player_x - my_position[0]) + abs(player_y - my_position[1])
    
    return tuple(min(enemies, key=distance_to_me)["pos"])

def danger_cells(enemy_position):
    cells = set()
    for dx, dy in MOVES.values():
        cells.add((enemy_position[0] + dx, enemy_position[1] + dy))
    return cells


def get_move(state):
    width, height = state["width"], state["height"]

    my_position = tuple(state["players"][state["you"]]["pos"])
    my_direction = state["your_direction"]

    enemy_position = find_enemy(state, my_position)
    if enemy_position is None:
        return my_direction

    walls = set(state["walls"])
    danger = danger_cells(enemy_position)

    best_move = None
    best_score = None
    for direction, (dx, dy) in MOVES.items():
        if direction == OPPOSITE[my_direction]:
            continue
        next_cell = (my_position[0] + dx, my_position[1] + dy)
        if not in_bounds(next_cell[0], next_cell[1], width, height):
            continue
        if next_cell in walls:
            continue
        score = territory(next_cell, enemy_position, walls, width, height)
        if next_cell in danger:
            score -= 15
        if best_score is None or score > best_score:
            best_move = direction
            best_score = score
    return best_move or my_direction

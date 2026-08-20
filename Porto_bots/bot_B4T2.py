from collections import deque


BOT_NAME = "B4T2"
BOT_COLOR = "#68ff03"
MOVES = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}


def get_neighbors(pos: tuple[int, int], walls: set[tuple[int, int]],
                  width: int, height: int) -> list[tuple[int, int]]:
    x, y = pos
    result = []
    for direction, (dx, dy) in MOVES.items():
        nx = x + dx
        ny = y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
            result.append((nx, ny))
    return result


def bfs_path(pos: tuple[int, int], walls: set[tuple[int, int]], width: int,
             height: int) -> dict[tuple[int, int], tuple[int, int] | None]:

    came_from: dict[tuple[int, int], tuple[int, int] | None] = {}
    queue = deque([pos])
    came_from[pos] = None

    while len(queue) > 0:
        current1 = queue.popleft()
        for neighbor in get_neighbors(current1, walls, width, height):
            if neighbor not in came_from:
                came_from[neighbor] = current1
                queue.append(neighbor)

    return came_from


def get_move(state):
    me = state["players"][state["you"]]
    x, y = me["pos"]
    walls = state["walls"]
    width, height = state["width"], state["height"]
    my_dir = state["your_direction"]

    best_move, best_score = None, -1
    for direction, (dx, dy) in MOVES.items():
        if direction == OPPOSITE[my_dir]:
            continue
        nx, ny = x + dx, y + dy
        if not (0 < nx < width and 0 <= ny < height) or (nx, ny) in walls:
            continue
        score = len(bfs_path((nx, ny), walls, width, height))
        if score > best_score:
            best_move, best_score = direction, score

    return best_move


# def main():
#     print(get_neighbors((10, 10), set(), 20, 20))
#     print(get_neighbors((0, 0), set(), 20, 20))
#     print(get_neighbors((0, 0), {(1, 0)}, 20, 20))

#     result = bfs_path((2, 2), set(), 20, 20)
#     print('Reachable cells:', len(result))
#     print('Entry:', result[(2, 2)])
#     print('Neighbors:', result[(3, 2)])


# if __name__ == "__main__":
#     main()

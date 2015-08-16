
from time import sleep
from copy import deepcopy
from random import randrange

from structures import Matrix


maze_map = """
..###........
#.#...######.
#.#..#.....#.
#.#.##.###.#.
#.#........#.
#.#.###.####.
#.#.#......#.
....########.
"""

maze = Matrix([[({'#': 1, '.': 0})[c] for c in r] for r in maze_map.split()])

rows = 8
cols = 13
start = (0, 0)
end = (7, 12)
visited = 2
on_path = 3
maze.bind_color(visited, 0x0000ff)
maze.bind_color(on_path, 0x00ff00)
maze.bind('pos', 0xff0000)

def dfs(pos=start):
    if not (0 <= pos[0] < rows and 0 <= pos[1] < cols) or maze[pos]:
        return False
    maze[pos] = on_path
    if pos == end:
        return True
    dirs = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    for dx, dy in dirs:
        if dfs((pos[0] + dx, pos[1] + dy)):
            return True
    maze[pos] = visited
    return False

dfs()


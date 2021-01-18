import random

wall = "w"
cell = "c"

def random_mouse(maze, entrance, exit):
    visited = []
    height, width = len(maze), len(maze[0])
    row, column = entrance
    while (row, column) != exit:
        visited.append((row, column))
        possible = []
        if row != 0:
            # check top
            if maze[row - 1][column] != wall:
                possible.append((row - 1, column))
        if row != height - 1:
            #check bottom
            if maze[row + 1][column] != wall:
                possible.append((row + 1, column))
        if column != 0:
            # check left
            if maze[row][column - 1] != wall:
                possible.append((row, column - 1))
        if column != width - 1:
            #check right
            if maze[row][column + 1] != wall:
                possible.append((row, column + 1))
        if len(possible) > 1:
            try:
                possible.remove(visited[-2])
            except:
                pass
        row, column = random.choice(possible)
    visited.append(exit)
    return visited






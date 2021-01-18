import random
import cv2 as cv
import numpy as np

cell = "c"
wall = "w"
unvisited = "u"


def dfs_neighbour_check(maze, width, height, current_width, current_height):
    neighbours = []
    if 0 <= current_height - 2:
        if maze[current_height - 2][current_width] == unvisited:
            neighbours.append([(current_height - 1, current_width), (current_height - 2, current_width)])
    if height-1 >= current_height + 2:
        if maze[current_height + 2][current_width] == unvisited:
            neighbours.append([(current_height + 1, current_width), (current_height + 2, current_width)])
    if 0 <= current_width - 2:
        if maze[current_height][current_width - 2] == unvisited:
            neighbours.append([(current_height, current_width - 1), (current_height, current_width - 2)])
    if width-1 >= current_width + 2:
        if maze[current_height][current_width + 2] == unvisited:
            neighbours.append([(current_height, current_width + 1), (current_height, current_width + 2)])
    random.shuffle(neighbours)
    return neighbours


def init_maze(width, height):
    maze = []
    walls_stack = []

    # initial maze with unvisited cells
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    starting_height = random.randint(1, height - 2)
    starting_width = random.randint(1, width - 2)

    maze[starting_height][starting_width] = cell

    walls_stack.extend(dfs_neighbour_check(maze, width, height, starting_width, starting_height))

    while walls_stack:
        new_cells = walls_stack.pop()
        if maze[new_cells[1][0]][new_cells[1][1]] == unvisited:
            maze[new_cells[0][0]][new_cells[0][1]] = cell
            maze[new_cells[1][0]][new_cells[1][1]] = cell
            walls_stack.extend(dfs_neighbour_check(maze, width, height, new_cells[1][1], new_cells[1][0]))

    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == unvisited:
                maze[i][j] = wall

    return (maze)

def create_maze_png(maze):
    maze = np.array(maze)
    white = (255, 255, 255)
    black = (0, 0, 0)
    special = (200, 0, 200)
    img = np.array([[white if j == cell else black for j in i] for i in maze])
    random_end = False
    maze_shape = maze.shape
    while not random_end:
        random_row = np.random.randint(maze_shape[0])
        random_col = np.random.randint(maze_shape[0])
        if (img[random_row][random_col] == white).all():
            img[random_row][random_col] = special
            random_end = True
    cv.imwrite("maze.png", img)


m = init_maze(120, 75)
create_maze_png(m)

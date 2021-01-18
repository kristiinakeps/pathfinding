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
    if height - 1 >= current_height + 2:
        if maze[current_height + 2][current_width] == unvisited:
            neighbours.append([(current_height + 1, current_width), (current_height + 2, current_width)])
    if 0 <= current_width - 2:
        if maze[current_height][current_width - 2] == unvisited:
            neighbours.append([(current_height, current_width - 1), (current_height, current_width - 2)])
    if width - 1 >= current_width + 2:
        if maze[current_height][current_width + 2] == unvisited:
            neighbours.append([(current_height, current_width + 1), (current_height, current_width + 2)])
    random.shuffle(neighbours)
    return neighbours


def upper_status(height_pixel, width_pixel, maze):
    if height_pixel > 0:
        return maze[height_pixel - 1][width_pixel]
    else:
        return False


def lower_status(height_pixel, width_pixel, maze, height):
    if height_pixel < height - 1:
        return maze[height_pixel + 1][width_pixel]
    else:
        return False


def left_status(height_pixel, width_pixel, maze):
    if width_pixel > 0:
        return maze[height_pixel][width_pixel - 1]
    else:
        return False


def right_status(height_pixel, width_pixel, maze, width):
    if width_pixel < width - 1:
        return maze[height_pixel][width_pixel + 1]
    else:
        return False


def delete_random_walls(percent, maze, wall_nr):
    height, width = len(maze), len(maze[0])
    nr_of_walls = wall_nr * percent
    while nr_of_walls > 0:
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        if maze[y][x] == wall:
            upper_s = upper_status(y, x, maze)
            lower_s = lower_status(y, x, maze, height)
            left_s = left_status(y, x, maze)
            right_s = right_status(y, x, maze, width)
            if upper_s and lower_s and left_s and right_s:
                if (upper_s == cell and lower_s == cell and left_s == wall and right_s == wall) or (
                        upper_s == wall and lower_s == wall and left_s == cell and right_s == cell) or (
                        upper_s == cell and lower_s == cell and left_s == cell and right_s == cell):
                    maze[y][x] = cell
                    nr_of_walls -= 1


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

    wallcounter = 0

    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == unvisited:
                maze[i][j] = wall
                wallcounter += 1

    delete_random_walls(0.05, maze, wallcounter)

    return maze


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

import random
import cv2 as cv
import numpy as np

# maze generation https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

cell = "c"
wall = "w"
unvisited = "u"

def init_maze(width, height):
    maze = []
    walls = []

    # initial maze with unvisited cells
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    starting_height = random.randint(1, height-2)
    starting_width = random.randint(1, width-2)

    maze[starting_height][starting_width] = cell

    walls.append((starting_height - 1, starting_width))
    walls.append((starting_height, starting_width - 1))
    walls.append((starting_height, starting_width + 1))
    walls.append((starting_height + 1, starting_width))

    maze[starting_height - 1][starting_width] = wall
    maze[starting_height][starting_width - 1] = wall
    maze[starting_height][starting_width + 1] = wall
    maze[starting_height + 1][starting_width] = wall

    while (walls):
        rand_wall_index = random.randint(0, len(walls)-1)
        rand_wall = walls[rand_wall_index]

        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1] - 1] == unvisited and maze[rand_wall[0]][rand_wall[1] + 1] == cell):
                cells = surrounding_cells(rand_wall, maze)
                if (cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    check_top_cell(maze, rand_wall, walls)
                    check_bottom_cell(maze, rand_wall, walls, height)
                    check_left_cell(maze, rand_wall, walls)
                delete_wall(rand_wall_index, walls)

                continue

        if (rand_wall[0] != 0):
            if (maze[rand_wall[0] - 1][rand_wall[1]] == unvisited and maze[rand_wall[0] + 1][rand_wall[1]] == cell):
                cells = surrounding_cells(rand_wall, maze)
                if (cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    check_top_cell(maze, rand_wall, walls)
                    check_left_cell(maze, rand_wall, walls)
                    check_right_cell(maze, rand_wall, walls, width)

                delete_wall(rand_wall_index, walls)
                continue

        # Check the bottom wall
        if (rand_wall[0] != height - 1):
            if (maze[rand_wall[0] + 1][rand_wall[1]] == unvisited and maze[rand_wall[0] - 1][rand_wall[1]] == cell):
                cells = surrounding_cells(rand_wall, maze)
                if (cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    check_bottom_cell(maze, rand_wall, walls, height)
                    check_left_cell(maze, rand_wall, walls)
                    check_right_cell(maze, rand_wall, walls, width)

                delete_wall(rand_wall_index, walls)
                continue

        # Check the right wall
        if (rand_wall[1] != width - 1):
            if (maze[rand_wall[0]][rand_wall[1] + 1] == unvisited and maze[rand_wall[0]][rand_wall[1] - 1] == cell):
                cells = surrounding_cells(rand_wall, maze)
                if (cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    check_right_cell(maze, rand_wall, walls, width)
                    check_bottom_cell(maze, rand_wall, walls, height)
                    check_top_cell(maze, rand_wall, walls)

                delete_wall(rand_wall_index, walls)
                continue

        delete_wall(rand_wall_index, walls)

    # remaining unvisited cells will become walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == unvisited):
                maze[i][j] = wall

    # entrance
    for i in range(0, width):
        if (maze[1][i] == cell):
            maze[0][i] = cell
            break
    # exit
    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == cell):
            maze[height - 1][i] = cell
            break

    return maze

def surrounding_cells(rand_wall, maze):
    cells = 0
    if (maze[rand_wall[0]-1][rand_wall[1]] == cell):
        cells += 1
    if (maze[rand_wall[0]+1][rand_wall[1]] == cell):
        cells += 1
    if (maze[rand_wall[0]][rand_wall[1]-1] == cell):
        cells +=1
    if (maze[rand_wall[0]][rand_wall[1]+1] == cell):
        cells += 1
    return cells

def check_right_cell(maze, rand_wall, walls, width):
    if (rand_wall[1] != width - 1):
        if (maze[rand_wall[0]][rand_wall[1] + 1] != cell):
            maze[rand_wall[0]][rand_wall[1] + 1] = wall
        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
            walls.append([rand_wall[0], rand_wall[1] + 1])

def check_left_cell(maze, rand_wall, walls):
    if (rand_wall[1] != 0):
        if (maze[rand_wall[0]][rand_wall[1] - 1] != cell):
            maze[rand_wall[0]][rand_wall[1] - 1] = wall
        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
            walls.append([rand_wall[0], rand_wall[1] - 1])

def check_top_cell(maze, rand_wall, walls):
    if (rand_wall[0] != 0):
        if (maze[rand_wall[0] - 1][rand_wall[1]] != cell):
            maze[rand_wall[0] - 1][rand_wall[1]] = wall
        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
            walls.append([rand_wall[0] - 1, rand_wall[1]])

def check_bottom_cell(maze, rand_wall, walls, height):
    if (rand_wall[0] != height - 1):
        if (maze[rand_wall[0] + 1][rand_wall[1]] != cell):
            maze[rand_wall[0] + 1][rand_wall[1]] = wall
        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
            walls.append([rand_wall[0] + 1, rand_wall[1]])


def delete_wall(rand_wall_index, walls):
    walls.pop(rand_wall_index)

def delete_random_walls(nr_of_walls, maze):
    height, width = len(maze), len(maze[0])
    while nr_of_walls > 0:
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        if maze[y][x] == wall:
            maze[y][x] = cell
            nr_of_walls -= 1

def create_maze_png(maze):
    white = (255, 255, 255)
    black = (0, 0, 0)
    img = np.array([[white if j == cell else black for j in i] for i in maze])
    cv.imwrite("maze.png", img)


maze = init_maze(70, 50)
delete_random_walls(500, maze)
create_maze_png(maze)

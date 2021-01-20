import random
import cv2 as cv
import numpy as np

cell = "c"
wall = "w"
unvisited = "u"
sea = "s"
desert = "d"
ice = "i"
end = "e"
start = "t"

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

    # delete_random_walls(0.05, maze, wallcounter)
    start_coord, end_coord = add_endtrance_and_exit_for_maze_path_finers(maze) # add_entrance_and_exit(maze)
    return maze,start_coord,end_coord


## maze_generation.py  copy start

def color_random_areas(nr_of_areas, maze):
    colors = [sea, desert, ice]
    shapes = ["diamond", "rectangle", "line"]
    for i in range(nr_of_areas):
        color = random.choice(colors)
        shape = random.choice(shapes)
        if shape == "diamond":
            draw_diamond(maze, color)
        elif shape == "rectangle":
            draw_rectangle(maze, color)
        else:
            draw_line(maze, color)


def draw_diamond(maze, color):
    height, width = len(maze), len(maze[0])
    max_shape_size = min(height, width) // 3 + (0 if (min(height, width) // 3) % 2 == 1 else 1)
    size = random.randint(5, max_shape_size)
    y = random.randint(0, height - 1 - size)
    x = random.randint(0, width - 1 - size)
    middle = size // 2
    to_color = 1
    for i in range(size):
        if i < middle:
            for j in range(middle - i, middle - i + to_color):
                if maze[y + i][x + j] == cell:
                    maze[y + i][x + j] = color
            to_color += 2
        if i == middle:
            for j in range(size):
                if maze[y + i][x + j] == cell:
                    maze[y + i][x + j] = color
            to_color -= 2
        if i > middle:
            for j in range(i - middle, i - middle + to_color):
                if maze[y + i][x + j] == cell:
                    maze[y + i][x + j] = color
            to_color -= 2


def draw_line(maze, color):
    height, width = len(maze), len(maze[0])
    if random.randint(1, 2) == 1:
        y = random.randint(0, height - 1)
        for i in range(width):
            if maze[y][i] == cell:
                maze[y][i] = color
    else:
        x = random.randint(0, width - 1)
        for i in range(height):
            if maze[i][x] == cell:
                maze[i][x] = color


def draw_rectangle(maze, color):
    height, width = len(maze), len(maze[0])
    height_size = random.randint(5, height // 3)
    width_size = random.randint(5, width // 3)
    y = random.randint(0, height - 1 - height_size)
    x = random.randint(0, width - 1 - width_size)

    for i in range(height_size):
        for j in range(width_size):
            if maze[y + i][x + j] == cell:
                maze[y + i][x + j] = color


def color_pixels(maze, visited=None):
    # BGR colors
    if visited is None:
        visited = []
    colormap = {cell: (255, 255, 255),
                wall: (0, 0, 0),
                desert: (102, 204, 255),
                sea: (255, 204, 102),
                ice: (255, 153, 204),
                end: (200, 0, 200),
                start: (0, 255, 0)
                }
    visited_colormap = {cell: (166, 166, 166),
                        wall: (0, 0, 0),
                        desert: (137, 202, 203),
                        sea: (110, 104, 80),
                        ice: (110, 80, 109),
                        end: (200, 0, 200),
                        start: (153, 0, 0)
                        }
    maze = np.array(maze)
    img = np.array([[colormap[j] for j in i] for i in maze])
    for row, column in visited:
        img[row, column] = visited_colormap[maze[row][column]]
    return img


def add_entrance_and_exit(maze):
    start_coord = add_random_point(maze, start)
    end_coord = add_random_point(maze, end)
    return start_coord, end_coord

def add_endtrance_and_exit_for_maze_path_finers(maze):
    height, width = len(maze), len(maze[0])

    #add dark edges
    add_first_row = 1 if maze[0].count(cell) > 0 else 0
    add_last_row = 1 if maze[height - 1].count(cell) > 0 else 0
    add_first_column = 1 if [maze[i][0] for i in range(len(maze))].count(cell) > 0 else 0
    add_last_column = 1 if [maze[i][width - 1] for i in range(len(maze))].count(cell) > 0 else 0

    height += add_first_row + add_last_row
    if add_last_row == 1:
        maze.append([wall for i in range(width)])
    if add_first_row == 1:
        maze.insert(0, [wall for i in range(width)])
    for i in range(height):
        if add_first_column == 1:
            maze[i].insert(0, wall)
        if add_last_column == 1:
            maze[i].append(wall)

    height, width = len(maze), len(maze[0])
    entrance = None
    for i in range(0, width):
        if (maze[1][i] == cell):
            maze[0][i] = cell
            entrance = (0, i)
            break
    exit = None
    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == cell):
            maze[height - 1][i] = cell
            exit = (height - 1, i)
            break
    return entrance, exit

def add_random_point(maze, marker):
    height, width = len(maze), len(maze[0])
    coordinates = None
    while coordinates is None:
        random_row = np.random.randint(height)
        random_col = np.random.randint(width)
        if (maze[random_row][random_col] == cell):
            maze[random_row][random_col] = marker
            coordinates = (random_row, random_col)
    return coordinates


## maze_generation.py  copy end


def create_maze_png(maze, filename, visited=None, special=True):
    maze = np.array(maze)
    maze_copy = maze.copy()
    if special:
        color_random_areas(6, maze_copy)
    if visited is None:
        visited = []
    img = color_pixels(maze_copy, visited)
    cv.imwrite(filename, img)


maze, start_hw, end_hw = init_maze(101, 101)
print(start_hw, end_hw)
create_maze_png(maze, "maze1.png")
create_maze_png(maze, "maze2.png", special=False)

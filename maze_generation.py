import random
import cv2 as cv
import numpy as np

# maze generation https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

cell = "c"
wall = "w"
unvisited = "u"
sea = "s"
desert = "d"
ice = "i"
end = "e"
start = "t"
single_mark = "*"
double_mark = "x"

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
    wallcounter = 0
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == unvisited):
                maze[i][j] = wall
                wallcounter+=1

    # entrance
    entrance = None
    for i in range(0, width):
        if (maze[1][i] == cell):
            maze[0][i] = cell
            entrance = (0, i)
            break
    # exit
    exit = None
    for i in range(width - 1, 0, -1):
        if (maze[height - 2][i] == cell):
            maze[height - 1][i] = cell
            exit = (height - 1, i)
            break

    #return maze, entrance, exit
    return maze,wallcounter

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
    height_size = random.randint(5, height//3)
    width_size = random.randint(5, width//3)
    y = random.randint(0, height - 1 - height_size)
    x = random.randint(0, width - 1 - width_size)

    for i in range(height_size):
        for j in range(width_size):
            if maze[y + i][x + j] == cell:
                maze[y + i][x + j] = color

def add_entrance_and_exit(maze):
    start_coord = add_random_point(maze, start)
    end_coord = add_random_point(maze, end)
    return start_coord, end_coord


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


def make_into_world(maze):
    start_coord, end_coord = add_entrance_and_exit(maze)
    wallcounter = 0

    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == unvisited:
                maze[i][j] = wall
                wallcounter += 1
    delete_random_walls(0.05, maze,wallcounter)
    color_random_areas(6, maze)
    return start_coord, end_coord

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
                start: (0, 255, 0),
                single_mark: (120, 239, 200),
                double_mark: (120, 173, 239)
                }
    visited_colormap = {cell: (166, 166, 166),
                wall: (0, 0, 0),
                desert: (137, 202, 203),
                sea: (110, 104, 80),
                ice: (110, 80, 109),
                end: (200, 0, 200),
                start: (80, 165, 0),
                single_mark: (120, 239, 200),
                double_mark: (120, 173, 239)
                }
    maze = np.array(maze)
    img = np.array([[colormap[j] for j in i] for i in maze])
    for row, column in visited:
        img[row, column] = visited_colormap[maze[row][column]]
    return img

def create_maze_png(maze, filename, visited=None):
    if visited is None:
        visited = []
    img = color_pixels(maze, visited)
    cv.imwrite(filename, img)
    return np.array(img, dtype="uint8")


#maze, entrance, exit = init_maze(30, 30)
#starting_v,ending_v = make_into_world(maze)
#start_coord, end_coord = make_into_world(maze)
#create_maze_png(maze, "maze.png")

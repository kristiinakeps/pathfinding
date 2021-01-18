import random

wall = "w"
cell = "c"

left = "left"
right = "right"
up = "up"
down = "down"

def random_mouse(maze, entrance, exit):
    visited = []
    row, column = entrance
    while (row, column) != exit:
        visited.append((row, column))
        possible = find_possible_moves(maze, row, column)
        if len(possible) > 1:
            try:
                possible.remove(visited[-2])
            except:
                pass
        row, column = random.choice(possible)
    visited.append(exit)
    return visited

def wall_follower(maze, entrance, exit):
    visited = []
    row, column = entrance
    while (row, column) != exit:
        visited.append((row, column))
        possible = find_possible_moves(maze, row, column)
        if len(visited) == 1:
            direction = right
        else:
            direction = determine_direction(row, column, visited[-2][0], visited[-2][1])
        row, column = find_new_direction(row, column, direction, possible)
    visited.append(exit)
    return visited


def determine_direction(row, column, prev_row, prev_column):
    if row == prev_row - 1:
        return up
    elif row == prev_row + 1:
        return down
    elif column == prev_column - 1:
        return left
    elif column == prev_column + 1:
        return right

def find_new_direction(row, column, direction, possible):
    if direction == right:
        turn_right = (row + 1, column)
        go_forward = (row, column + 1)
        turn_left = (row - 1, column)
    elif direction == left:
        turn_right = (row - 1, column)
        go_forward = (row, column - 1)
        turn_left = (row + 1, column)
    elif direction == up:
        turn_right = (row, column + 1)
        go_forward = (row - 1, column)
        turn_left = (row, column - 1)
    else:
        turn_right = (row, column - 1)
        go_forward = (row + 1, column)
        turn_left = (row, column + 1)

    if turn_right in possible:
        return turn_right
    if go_forward in possible:
        return go_forward
    if turn_left in possible:
        return turn_left
    else:
        return possible[0]



def find_possible_moves(maze, row, column):
    height, width = len(maze), len(maze[0])
    possible = []
    if row != 0:
        # check top
        if maze[row - 1][column] != wall:
            possible.append((row - 1, column))
    if row != height - 1:
        # check bottom
        if maze[row + 1][column] != wall:
            possible.append((row + 1, column))
    if column != 0:
        # check left
        if maze[row][column - 1] != wall:
            possible.append((row, column - 1))
    if column != width - 1:
        # check right
        if maze[row][column + 1] != wall:
            possible.append((row, column + 1))
    return possible







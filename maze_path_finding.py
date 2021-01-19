import random

wall = "w"
cell = "c"

left = "left"
right = "right"
up = "up"
down = "down"
forward = "continue"
back = "backwards"

single_mark = "*"
double_mark = "x"

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
            direction = down
        else:
            direction = determine_direction(row, column, visited[-2][0], visited[-2][1])
        (row, column), heading = find_new_direction(row, column, direction, possible)
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
        return turn_right, right
    if go_forward in possible:
        return go_forward, forward
    if turn_left in possible:
        return turn_left, left
    else:
        return possible[0], back



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

def pledge(maze, entrance, exit):
    visited = []
    row, column = entrance
    degrees_turned = 0
    while (row, column) != exit:
        visited.append((row, column))
        # if degrees_turned is 0, then move down, if we face an obsticle, then we do wall following with right hand
        possible = find_possible_moves(maze, row, column)
        if degrees_turned == 0 and (row + 1, column) in possible:
            row += 1
        else:
            direction = determine_direction(row, column, visited[-2][0], visited[-2][1])
            (row, column), heading = find_new_direction(row, column, direction, possible)
            if heading == right:
                degrees_turned += 90
            elif heading == left:
                degrees_turned -= 90
            elif heading == back:
                degrees_turned -= 180
    visited.append(exit)
    return visited

def recursive(maze, entrance, exit):
    visited = []
    recursive_search(maze, entrance[0], entrance[1], exit, visited)
    visited.append(exit)
    return visited

def recursive_search(maze, row, column, exit, visited):
    if (row, column) == exit:
        return True
    if maze[row][column] == wall or (row, column) in visited:
        return False
    visited.append((row, column))
    possible = find_possible_moves(maze, row, column)
    for r, c in possible:
        if recursive_search(maze, r, c, exit, visited):
            return True
    return False







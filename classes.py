import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import heapq
import copy
from datetime import datetime


class vertex:
    def __init__(self, h_pic, w_pic, value):
        self.height = h_pic
        self.width = w_pic
        self.distance = sys.maxsize
        self.value = value
        self.previous = None
        self.processed = False

    def __lt__(self, other):
        return self.distance < other.distance


def establishVertices(maze_file, first_vertex):
    maze = cv2.imread(maze_file)
    height, width, _ = maze.shape
    plt.imshow(cv2.cvtColor(maze, cv2.COLOR_BGR2RGB))
    image_vertices = np.full((height, width), None)

    for i in range(height):
        for j in range(width):
            image_vertices[i, j] = vertex(i, j, maze[i, j])
            if i == first_vertex[0] and j == first_vertex[1]:  # starting point
                image_vertices[i, j].distance = 0
            elif (maze[i, j] == [0, 0, 0]).all():  # barriers
                image_vertices[i, j].processed = True
    return maze, image_vertices


def distanceFunc(current, element, end, algoName, maze, colormap):
    move_value = colormap[tuple(maze[element.height][element.width])]
    if algoName == "dijkstra":
        return current.distance + move_value * (
            np.sqrt((current.height - element.height) ** 2 + (current.width - element.width) ** 2))
    if algoName == "astar":
        return current.distance + move_value * (
            np.sqrt((current.height - element.height) ** 2 + (current.width - element.width) ** 2)) + np.sqrt(
            (end[0] - element.height) ** 2 + (end[1] - element.width) ** 2)
    else:
        return None


def mazeAlgorithm(starting_vertex, algo_name, maze, image_vertices, end, show_visual):
    colormap = {(102, 204, 255): 2,
                (255, 204, 102): 4,
                (255, 153, 204): 0.5,
                (255, 255, 255): 1}
    visited_colormap = {(255, 255, 255): (166, 166, 166),
                        (102, 204, 255): (137, 202, 203),
                        (255, 204, 102): (110, 104, 80),
                        (255, 153, 204): (110, 80, 109),
                        (200, 0, 200): (200, 0, 200),
                        (0, 255, 0): (80, 165, 0)
                        }
    height, width, _ = maze.shape
    # for video :
    # out = cv2.VideoWriter(algo_name + str(np.random.randint(100)) + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), 200, (width*4,height*4))
    gone_through = []
    to_process = []
    start_time = datetime.now()
    continue_finding = True
    current = image_vertices[starting_vertex]
    gone_through.append(current)
    while continue_finding:
        h_current = current.height
        w_current = current.width
        #        upperb_x = False
        #        lowerb_x = False
        #        upperb_y = False
        #        lowerb_y = False
        neighbours = []
        if h_current > 0 and not image_vertices[h_current - 1, w_current].processed:
            #            lowerb_x = True
            neighbours.append(image_vertices[h_current - 1, w_current])
        if h_current < height - 1 and not image_vertices[h_current + 1, w_current].processed:
            #            upperb_x = True
            neighbours.append(image_vertices[h_current + 1, w_current])
        if w_current > 0 and not image_vertices[h_current, w_current - 1].processed:
            #            lowerb_y = True
            neighbours.append(image_vertices[h_current, w_current - 1])
        if w_current < width - 1 and not image_vertices[h_current, w_current + 1].processed:
            neighbours.append(image_vertices[h_current, w_current + 1])
        #            upperb_y = True
        # ma jatsin diagonaalide vaatamise valja prg
        #        if lowerb_x and lowerb_y and not image_vertices[h_current - 1, w_current - 1].processed:
        #            neighbours.append(image_vertices[h_current - 1, w_current - 1])
        #        if lowerb_x and upperb_y and not image_vertices[h_current - 1, w_current + 1].processed:
        #            neighbours.append(image_vertices[h_current - 1, w_current + 1])
        #        if upperb_x and lowerb_y and not image_vertices[h_current + 1, w_current - 1].processed:
        #            neighbours.append(image_vertices[h_current + 1, w_current - 1])
        #        if upperb_x and upperb_y and not image_vertices[h_current + 1, w_current + 1].processed:
        #            neighbours.append(image_vertices[h_current + 1, w_current + 1])
        for element in neighbours:
            if (element.value == [200, 0, 200]).all():
                continue_finding = False
                element.previous = current
                break
            else:
                if algo_name in ('depthfirst', 'breadthfirst'):
                    to_process.append((element.distance, element))
                else:
                    new_dist = distanceFunc(current, element, end, algo_name, maze, colormap)
                    if new_dist < element.distance:
                        heapq.heappush(to_process, (new_dist, element))
                        element.distance = new_dist
                        element.previous = current
        current.processed = True
        maze[h_current, w_current] = visited_colormap[tuple(maze[h_current, w_current])]
        if show_visual:
            maze_big = cv2.resize(maze, (maze.shape[1] * 4, maze.shape[0] * 4), interpolation=cv2.INTER_AREA)
            cv2.imshow(algo_name, maze_big)
            cv2.waitKey(1)
            # for video :
            # out.write(maze_big)
        gone_through.append(current)
        while current.processed:
            if algo_name == 'depthfirst':
                dist, current = to_process.pop()
            elif algo_name == 'breadthfirst':
                dist, current = to_process.pop(0)
            else:
                dist, current = heapq.heappop(to_process)

    end_time = datetime.now()
    path = element.previous
    while path is not None:
        maze[path.height, path.width] = [0, 0, 255]
        maze_big = cv2.resize(maze, (maze.shape[1] * 4, maze.shape[0] * 4), interpolation=cv2.INTER_AREA)
        cv2.imshow(algo_name, maze_big)
        cv2.waitKey(1)
        # for video :
        # out.write(maze_big)
        path = path.previous
    # for video :
    # out.release()
    print('Duration: {}'.format(end_time - start_time))
    return element, gone_through


def create_files(last_element, coverage_elements, algo_name):
    prev = last_element.previous
    file_name_1 = algo_name + '_path.txt'
    f = open(file_name_1, "w+")
    while prev is not None:
        f.write(str(prev.width) + ' ' + str(prev.height) + '\n')
        prev = prev.previous
    f.close()
    file_name_2 = algo_name + '_coverage.txt'
    f = open(file_name_2, "w+")
    for element in coverage_elements:
        f.write(str(element.width) + ' ' + str(element.height) + '\n')
    f.close()


def save_pic(maze, nr):
    maze = cv2.resize(maze, (maze.shape[1] * 4, maze.shape[0] * 4), interpolation=cv2.INTER_AREA)
    cv2.imwrite('color_img' + str(nr) + '.png', maze)


# dijkstra

first = (10, 59)
end = (84, 58)

maze, image_vertices = establishVertices("maze1.png", first)
last, coverage = mazeAlgorithm(first, 'dijkstra', maze, image_vertices, end, True)
save_pic(maze, 1)
# create_files(last, coverage, 'dijkstra')

maze, image_vertices = establishVertices("maze2.png", first)
last, coverage = mazeAlgorithm(first, 'dijkstra', maze, image_vertices, end, False)
save_pic(maze, 2)

# A star

maze, image_vertices = establishVertices("maze1.png", first)
last, coverage = mazeAlgorithm(first, 'astar', maze, image_vertices, end, False)
save_pic(maze, 3)

maze, image_vertices = establishVertices("maze2.png", first)
last, coverage = mazeAlgorithm(first, 'astar', maze, image_vertices, end, False)
save_pic(maze, 4)

# Depth first search

maze, image_vertices = establishVertices("maze.png", first)
last, coverage = mazeAlgorithm(first, 'depthfirst', maze, image_vertices, end, False)

maze, image_vertices = establishVertices("maze.png", first)
last, coverage = mazeAlgorithm(first, 'breadthfirst', maze, image_vertices, end, False)

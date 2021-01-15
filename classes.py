import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import heapq
from datetime import datetime


class vertex:
    def __init__(self, x_pic, y_pic, value):
        self.x = x_pic
        self.y = y_pic
        self.distance = sys.maxsize
        self.value = value
        self.previous = None
        self.processed = False

    def __lt__(self, other):
        return self.distance < other.distance


def establishVertices(maze_file, first_vertex):
    maze = cv2.imread(maze_file)
    x_len, y_len, dummy = maze.shape
    plt.imshow(cv2.cvtColor(maze, cv2.COLOR_BGR2RGB))
    image_vertices = np.full((x_len, y_len), None)

    for i in range(x_len):
        for j in range(y_len):
            image_vertices[i, j] = vertex(i, j, maze[i, j])
            if i == first_vertex[0] and j == first_vertex[1]:  # starting point
                image_vertices[i, j].distance = 0
            elif (maze[i, j] == [0, 0, 0]).all():  # barriers
                image_vertices[i, j].processed = True
    return maze, image_vertices


def distanceFunc(current, element, end, algoName):
    if algoName == "dijkstra":
        return current.distance + np.sqrt((current.x - element.x) ** 2 + (current.y - element.y) ** 2)
    if algoName == "astar":
        return current.distance + np.sqrt((current.x - element.x) ** 2 + (current.y - element.y) ** 2) + np.sqrt(
            (end[0] - element.x) ** 2 + (end[1] - element.y) ** 2)
    else:
        return None


def mazeAlgorithm(starting_vertex, algo_name, maze, image_vertices, end, show_visual):
    x_len, y_len, dummy = maze.shape
    gone_through = []
    to_process = []
    start_time = datetime.now()
    continue_finding = True
    current = image_vertices[starting_vertex]
    gone_through.append(current)
    while continue_finding:
        x_current = current.x
        y_current = current.y
        upperb_x = False
        lowerb_x = False
        upperb_y = False
        lowerb_y = False
        neighbours = []
        if x_current > 0 and not image_vertices[x_current - 1, y_current].processed:
            lowerb_x = True
            neighbours.append(image_vertices[x_current - 1, y_current])
        if x_current < x_len - 1 and not image_vertices[x_current + 1, y_current].processed:
            upperb_x = True
            neighbours.append(image_vertices[x_current + 1, y_current])
        if y_current > 0 and not image_vertices[x_current, y_current - 1].processed:
            lowerb_y = True
            neighbours.append(image_vertices[x_current, y_current - 1])
        if y_current < y_len - 1 and not image_vertices[x_current, y_current + 1].processed:
            neighbours.append(image_vertices[x_current, y_current + 1])
            upperb_y = True
        if lowerb_x and lowerb_y and not image_vertices[x_current - 1, y_current - 1].processed:
            neighbours.append(image_vertices[x_current - 1, y_current - 1])
        if lowerb_x and upperb_y and not image_vertices[x_current - 1, y_current + 1].processed:
            neighbours.append(image_vertices[x_current - 1, y_current + 1])
        if upperb_x and lowerb_y and not image_vertices[x_current + 1, y_current - 1].processed:
            neighbours.append(image_vertices[x_current + 1, y_current - 1])
        if upperb_x and upperb_y and not image_vertices[x_current + 1, y_current + 1].processed:
            neighbours.append(image_vertices[x_current + 1, y_current + 1])
        for element in neighbours:
            if (element.value == [200, 0, 200]).all():
                continue_finding = False
                element.previous = current
                break
            else:
                if algo_name == 'depthfirst':
                    to_process.append((element.distance, element))
                else:
                    new_dist = distanceFunc(current, element, end, algo_name)
                    if new_dist < element.distance:
                        heapq.heappush(to_process, (new_dist, element))
                        element.distance = new_dist
                        element.previous = current
        current.processed = True
        maze[x_current, y_current] = [0, 200, 0]
        if show_visual:
            cv2.imshow(algo_name, maze)
            cv2.waitKey(1)
        gone_through.append(current)
        while current.processed:
            if algo_name == 'depthfirst':
                dist, current = to_process.pop()
            else:
                dist, current = heapq.heappop(to_process)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    return element, gone_through


def create_files(last_element, coverage_elements, algo_name):
    prev = last_element.previous
    file_name_1 = algo_name + '_path.txt'
    f = open(file_name_1, "w+")
    while prev is not None:
        f.write(str(prev.y) + ' ' + str(prev.x) + '\n')
        prev = prev.previous
    f.close()
    file_name_2 = algo_name + '_coverage.txt'
    f = open(file_name_2, "w+")
    for element in coverage_elements:
        f.write(str(element.y) + ' ' + str(element.x) + '\n')
    f.close()

# dijkstra

## koigil algus prg 2,2 aga pmst see voib ju must ka olla prg niiet siin voib errorit anda
first = (2, 2)
maze, image_vertices = establishVertices("maze.png", first)
end = [88, 23]
last, coverage = mazeAlgorithm(first, 'dijkstra', maze, image_vertices, end, True)
create_files(last, coverage, 'dijkstra')

# A star

first = (2, 2)
maze, image_vertices = establishVertices("maze1.png", first)
end = [88, 23]
last, coverage = mazeAlgorithm(first, 'astar', maze, image_vertices, end, True)

# Depth first search

first = (2, 2)
maze, image_vertices = establishVertices("maze1.png", first)
end = [88, 23]
last, coverage = mazeAlgorithm(first, 'depthfirst', maze, image_vertices, end, True)

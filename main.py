import maze_path_finding
import maze_generation


maze, entrance, exit = maze_generation.init_maze(30, 20)

mouse_visited = maze_path_finding.random_mouse(maze, entrance, exit)
wall_visited = maze_path_finding.wall_follower(maze, entrance, exit)
pledge_visited = maze_path_finding.pledge(maze, entrance, exit)
recursive_visited = maze_path_finding.recursive(maze, entrance, exit)

import copy
maze_tremaux = copy.deepcopy(maze)
tremaux_visited = maze_path_finding.tremaux(maze_tremaux, entrance, exit)

maze_generation.create_maze_png(maze, "mouse.png", visited=mouse_visited)
maze_generation.create_maze_png(maze, "wall.png", visited=wall_visited)
maze_generation.create_maze_png(maze, "pledge.png", visited=pledge_visited)
maze_generation.create_maze_png(maze, "recursive.png", visited=recursive_visited)

maze_generation.create_maze_png(maze_tremaux, "tremaux.png", visited=tremaux_visited)

import maze_path_finding
import maze_generation


maze, entrance, exit = maze_generation.init_maze(30, 20)
mouse_visited = maze_path_finding.random_mouse(maze, entrance, exit)
maze_generation.create_maze_png(maze, "mouse.png", visited=mouse_visited)
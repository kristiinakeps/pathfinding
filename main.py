import maze_path_finding
import maze_generation


maze, entrance, exit = maze_generation.init_maze(30, 20)

mouse_visited = maze_path_finding.random_mouse(maze, entrance, exit)
wall_visited = maze_path_finding.wall_follower(maze, entrance, exit)

maze_generation.create_maze_png(maze, "mouse.png", visited=mouse_visited)
maze_generation.create_maze_png(maze, "wall.png", visited=wall_visited)

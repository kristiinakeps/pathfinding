import maze_path_finding
import maze_generation
import dfs_gen
import time
import copy

maze, entrance, exit = maze_generation.init_maze(30, 20)
mouse_visited = maze_path_finding.random_mouse(maze, entrance, exit)
wall_visited = maze_path_finding.wall_follower(maze, entrance, exit)
pledge_visited = maze_path_finding.pledge(maze, entrance, exit)
recursive_visited = maze_path_finding.recursive(maze, entrance, exit)

maze_tremaux = copy.deepcopy(maze)
tremaux_visited = maze_path_finding.tremaux(maze_tremaux, entrance, exit)

maze_generation.create_maze_png(maze, "mouse.png", visited=mouse_visited)
maze_generation.create_maze_png(maze, "wall.png", visited=wall_visited)
maze_generation.create_maze_png(maze, "pledge.png", visited=pledge_visited)
maze_generation.create_maze_png(maze, "recursive.png", visited=recursive_visited)
maze_generation.create_maze_png(maze_tremaux, "tremaux.png", visited=tremaux_visited)


times_mouse = []
times_wall = []
times_pledge = []
times_recursive = []
times_tremaux = []

count_mouse = []
count_wall = []
count_pledge = []
count_recursive = []
count_tremaux = []


sizes =  [30, 70, 100]

for size in sizes:
    recursion_errors = []
    for i in range(100):
        print(i)
        # deleting walls in dfs_gen must be disabled
        maze, entrance, exit = maze_generation.init_maze(size, size) # dfs_gen.init_maze(size, size)

        start = time.perf_counter()
        mouse_visited = maze_path_finding.random_mouse(maze, entrance, exit)
        end = time.perf_counter()
        times_mouse.append(end - start)
        count_mouse.append(len(mouse_visited))

        start = time.perf_counter()
        wall_visited = maze_path_finding.wall_follower(maze, entrance, exit)
        end = time.perf_counter()
        times_wall.append(end - start)
        count_wall.append(len(wall_visited))

        start = time.perf_counter()
        maze_tremaux = copy.deepcopy(maze)
        tremaux_visited = maze_path_finding.tremaux(maze_tremaux, entrance, exit)
        end = time.perf_counter()
        times_tremaux.append(end - start)
        count_tremaux.append(len(tremaux_visited))

        start = time.perf_counter()
        pledge_visited = maze_path_finding.pledge(maze, entrance, exit)
        end = time.perf_counter()
        times_pledge.append(end - start)
        count_pledge.append(len(pledge_visited))

        try:
            start = time.perf_counter()
            recursive_visited = maze_path_finding.recursive(maze, entrance, exit)
            end = time.perf_counter()
            times_recursive.append(end - start)
            count_recursive.append(len(recursive_visited))
        except RecursionError:
            print("recutsion error at", i)
            recursion_errors.append(i)

    print("Size:", size)
    print("Mouse:", times_mouse, count_mouse)
    print("Wall:", times_wall, count_wall)
    print("Pledge:", times_pledge, count_pledge)
    print("Recursive", times_recursive, count_recursive)
    print("Tremaux:", times_tremaux, count_tremaux)
    print("Recursion errors:", recursion_errors)


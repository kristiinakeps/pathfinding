import maze_generation
import dfs_gen
import time
import numpy as np

sizes = [i for i in range(10, 500, 10)]
prims = {size: [] for size in sizes}
dfs = {size: [] for size in sizes}

for i in range(10):
    print(i)
    for size in sizes:
        start = time.perf_counter()
        _, _, _ = maze_generation.init_maze(size, size)
        end = time.perf_counter()
        prims[size].append(end - start)

        start = time.perf_counter()
        _, _, _ = dfs_gen.init_maze(size, size)
        end = time.perf_counter()
        dfs[size].append(end - start)

print("Prims:")
for size in prims:
    print(size, np.mean(prims[size]))
print("DFS:")
for size in dfs:
    print(size, np.mean(dfs[size]))


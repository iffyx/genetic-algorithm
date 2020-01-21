from random import randint
from random import seed
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import time
import os.path
import sys

import genetic_alg1
import genetic_alg2
import genetic_alg3
from maze_generator import generate_maze


def random_start_point():
    x, y = 0, 0
    # maze[1][0] = 0
    # maze[1][maze_size-1] = 1
    # maze[maze_size-1][1] = 1
    while maze[y][x] != 0:
        y = randint(5, 10)
        # y = 1
        # x = 0
        x = randint(5, 10)
    return y, x


def random_end_point():
    x, y = 0, 0
    # maze[maze_size-1][maze_size] = 0
    while maze[y][x] != 0:
        y = randint(maze_size-10, maze_size-5)
        # y = maze_size-1
        # x = maze_size
        x = randint(maze_size-10, maze_size-5)
    return y, x


def print_maze(best):
    i = 0
    actual_y = start_point[0]
    actual_x = start_point[1]
    for b in best:
        if b == 1:
            actual_y = actual_y - 1
        elif b == 2:
            actual_x = actual_x + 1
        elif b == 3:
            actual_y = actual_y + 1
        elif b == 4:
            actual_x = actual_x - 1

        if maze[actual_y][actual_x] == 1:
            if b == 1:
                actual_y = actual_y + 1
            elif b == 2:
                actual_x = actual_x - 1
            elif b == 3:
                actual_y = actual_y - 1
            elif b == 4:
                actual_x = actual_x + 1
            # b = 0
        maze[actual_y][actual_x] = 2
        if b != 0:
            i = i+1
        if (actual_y == end_point[0]) & (actual_x == end_point[1]):
            break

    maze[start_point[0]][start_point[1]] = 3
    maze[end_point[0]][end_point[1]] = 4
    print('moves', i)
    cmap = colors.ListedColormap(['white', 'black', 'red', 'green', 'blue'])

    plt.imshow(maze, cmap=cmap)
    plt.xticks([]), plt.yticks([])
    plt.show()


def run_chromosome2():
    chromosome_length = 20
    mate_rate = 0.5
    mutation_rate = 0.4
    iterations = 60
    population = 1000

    best, value, generation, pop, logbook = genetic_alg2.solve(maze, start_point, end_point, chromosome_length,
                                                               mate_rate,
                                                               mutation_rate, iterations, population)

    print(value[0])
    print_maze(best)


def run_chromosome1():
    chromosome_length = 700
    mate_rate = 0.5
    mutation_rate = 0.4
    iterations = 60
    population = 1000

    best, value, generation, pop, logbook = genetic_alg1.solve(maze, start_point, end_point, chromosome_length,
                                                               mate_rate,
                                                               mutation_rate, iterations, population)

    print(value[0])
    print_maze(best)


maze_size = int(sys.argv[1])


if os.path.exists('maze' + str(maze_size) + '.npy'):
    maze = np.load('maze' + str(maze_size) + '.npy')
else:
    maze = generate_maze(maze_size, maze_size)

start_point = random_start_point()
end_point = random_end_point()

run_chromosome1()
run_chromosome2()

print('start point', start_point[0], start_point[1])
print('end point', end_point[0], end_point[1])


# start = time.time()
# best, value, generation, pop, logbook = solve(maze, start_point, end_point, chromosome_length, mate_rate, mutation_rate, iterations, population)
# best, value, pop, logbook = solve(maze, start_point, end_point, chromosome_length, mate_rate, mutation_rate, iterations, population)
# end = time.time()
# print('GA time:', end - start, 'in generation', generation)

# print(value[0])
# print_maze()

# print(logbook)
#
# start = time.time()
# result = astar(maze2, start_point, end_point)
# end = time.time()
# print('A* time:', end - start)
#
# print('shortest path length', len(result))
# for x in result:
#     maze2[x[0]][x[1]] = 2
#
# maze2[start_point[0]][start_point[1]] = 3
# maze2[end_point[0]][end_point[1]] = 4
#
# cmap = colors.ListedColormap(['white', 'black', 'red', 'green', 'blue'])
# plt.imshow(maze2, cmap=cmap)
# plt.xticks([]), plt.yticks([])
# plt.show()
#

import random
from deap import base
from deap import creator
from deap import tools
import numpy as np
import math


def solve(maze, start_point, end_point, chromosome_length, mate_rate, mutation_rate, iterations, population):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_int", random.randint, 1, 4)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_int, chromosome_length)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def fitness(chromosome):
        actual_y = start_point[0]
        actual_x = start_point[1]
        for i in range(len(chromosome)):
            if chromosome[i]:
                if chromosome[i] == 1:
                    actual_y = actual_y - 1
                elif chromosome[i] == 2:
                    actual_x = actual_x + 1
                elif chromosome[i] == 3:
                    actual_y = actual_y + 1
                elif chromosome[i] == 4:
                    actual_x = actual_x - 1

                if maze[actual_y][actual_x] == 1:
                    value = (math.fabs(end_point[0] - actual_y) + math.fabs(end_point[1] - actual_x))
                    return [value]
            if (actual_y == end_point[0]) & (actual_x == end_point[1]):
                return [0]

        value = (math.fabs(end_point[0] - actual_y) + math.fabs(end_point[1] - actual_x))

        return [value]

    toolbox.register("evaluate", fitness)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=mutation_rate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=population)

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields
    logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
    print(logbook.stream)

    while min(fits) != 0 and g < iterations:
        g = g + 1
        # print(g, min(fits), max(fits), np.average(fits))

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < mate_rate:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_rate:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        # Gather all the fitnesses in one list
        fits = [ind.fitness.values[0] for ind in pop]

        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)

    best_ind = tools.selBest(pop, 1)[0]
    # print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    return best_ind, best_ind.fitness.values, g, pop, logbook

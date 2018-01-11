# -*- coding: utf-8 -*-
import population as p


class Solver_8_queens:
    def __init__(self, pop_size=1000, cross_prob=0.7, mut_prob=0.001):
        self.__population_size = pop_size
        self.__cross_prob = cross_prob
        self.__mut_prob = mut_prob

    def solve(self, min_fitness, max_epochs):
        if min_fitness is None and max_epochs is None:
            return 0, 0, None

        population = p.Population(self.__population_size)
        population.initialize(chromosome_size=8)

        epoch_num = 0
        best_result = None
        best_fitness = 0

        while True:
            if max_epochs is not None and epoch_num + 1 > max_epochs:
                break
            epoch_num += 1

            parents_population = population.selection(self.__population_size)
            children_population = []

            for i in range(self.__population_size / 2):
                children = population.crossover(parents_population, self.__cross_prob)
                if children is not None:
                    mutated_children = population.mutate(children, self.__mut_prob)
                    children_population.extend(mutated_children)
            population.reduction(children_population)

            result = population.getBestResult()

            if result.fitness > best_fitness:
                best_result = result.copy()
                best_fitness = result.fitness

            if population.isFinal(min_fitness):
                break

            #print("fitness: %.2f" % result.fitness,
            #      "epoch: %s" % epoch_num)

        return best_fitness, epoch_num, best_result

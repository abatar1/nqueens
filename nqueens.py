# -*- coding: utf-8 -*-
import population as p
import genetic_simulator as gs


class Solver_8_queens:
    def __init__(self, pop_size=1000, cross_prob=0.75, mut_prob=0.001):
        self._population_size = pop_size
        self._cross_prob = cross_prob
        self._mut_prob = mut_prob

    def solve(self, min_fitness, max_epochs):
        if min_fitness is None and max_epochs is None:
            return 0, 0, None

        initial_population = p.Population(self._population_size, chromosome_size=8)
        simulator = gs.GeneticSimulator(initial_population, self._cross_prob, self._mut_prob)

        while not simulator.is_end(max_epochs, min_fitness):
            simulator.step()
            #print(simulator.state)

        return simulator.best_result.fitness, simulator.epoch_num, simulator.best_result

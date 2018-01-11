import operator
import numpy as np
import chromosome as c


class Population:
    def __init__(self, population_size):
        self.chromosomes = []
        self.size = population_size
        self.total_fitness = 0

    def initialize(self, chromosome_size):
        max_conflicts = chromosome_size * (chromosome_size - 1) / 2
        bit_size = chromosome_size * 3

        self.chromosomes = [c.Chromosome(chromosome_size, bit_size, max_conflicts) for i in range(self.size)]
        for chromosome in self.chromosomes:
            chromosome.generateSequence()
            chromosome.calculateFitness()

    def extend(self, new_chromosomes):
        self.chromosomes.extend(new_chromosomes)
        self.size += len(new_chromosomes)

    def isFinal(self, min_fitness):
        if min_fitness == None:
            return False
        return any(x.fitness >= min_fitness for x in self.chromosomes)

    def getBestResult(self):
        return max(self.chromosomes, key=operator.attrgetter('fitness'))

    def __rouletteSelect(self):
        value = np.random.uniform(0, self.total_fitness)

        # I can refactor this to look more acceptable
        # but this version works fast enough
        if value < self.total_fitness / 2:
            probability_offset = 0
            for i in range(self.size):
                probability_offset += self.chromosomes[i].fitness
                if probability_offset >= value:
                    return self.chromosomes[i]
        else:
            probability_offset = self.total_fitness
            for i in range(self.size - 1, 0, -1):
                probability_offset -= self.chromosomes[i].fitness
                if probability_offset <= value:
                    return self.chromosomes[i]

    def selection(self, num):
        self.total_fitness = sum(c.fitness for c in self.chromosomes)
        return [self.__rouletteSelect() for _ in range(num)]

    def crossover(self, parents, cross_prob):
        if np.random.random_sample() > cross_prob:
            return None

        parent_indexes = np.random.random_integers(0, len(parents) - 1, 2)
        parent1, parent2 = parents[parent_indexes[0]], parents[parent_indexes[1]]

        crossing_over_point = np.random.random_integers(parent1.size - 1)

        return parent1.crossover(parent2, crossing_over_point)

    def reduction(self, new_population):
        for c in new_population:
            pos =  np.random.random_integers(0, self.size - 1)
            self.chromosomes[pos] = c.copy()

    def mutate(self, children, mut_prob):
        for child in children:
            if np.random.random_sample() > mut_prob:
                continue
            child.mutate()
        return children

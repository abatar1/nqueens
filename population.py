import operator
import random
from itertools import accumulate
import chromosome as c


class Population:
    def __init__(self, population_size, chromosome_size):
        self.size = population_size
        self.total_fitness = 0

        max_conflicts = chromosome_size * (chromosome_size - 1) / 2
        bit_size = chromosome_size * (chromosome_size.bit_length() - 1)

        self.chromosomes = [c.Chromosome(None, chromosome_size, bit_size, max_conflicts) for i in range(population_size)]

    def extend(self, new_chromosomes):
        self.chromosomes.extend(new_chromosomes)
        self.size += len(new_chromosomes)

    def is_final(self, min_fitness):
        if min_fitness is None:
            return False
        return any(x.fitness >= min_fitness for x in self.chromosomes)

    @property
    def best_result(self):
        return max(self.chromosomes, key=operator.attrgetter('fitness'))

    def selection(self):
        self.total_fitness = sum(c.fitness for c in self.chromosomes)

        fitnesses = list(accumulate([c.fitness for c in self.chromosomes]))
        result = []
        for i in range(self.size):
            value = random.random()
            for j in range(self.size):
                if fitnesses[j] > value:
                    result.append( self.chromosomes[j])
                    break
        return result

    def crossover(self, parents, cross_prob):
        if random.random() > cross_prob:
            return None

        parent_indexes = random.sample(range(len(parents) - 1), 2)
        parent1, parent2 = parents[parent_indexes[0]], parents[parent_indexes[1]]

        crossing_over_point = random.randint(0, parent1.size - 1)

        return parent1.crossover(parent2, crossing_over_point)

    def reduction(self, new_population):
        updating_positions = random.sample(range(1, self.size - 1), len(new_population))
        for i in range(1, len(new_population) - 1):
            self.chromosomes[updating_positions[i]] = new_population[i]

    def mutate(self, children, mut_prob):
        for child in children:
            if random.random() > mut_prob:
                continue
            child.mutate()
        return children

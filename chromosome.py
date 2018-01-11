import numpy as np
from bitarray import bitarray


class Chromosome:
    def __init__(self, chromosome_size, bit_size, max_conflicts):
        self.sequence = None
        self.fitness = 0
        self.size = chromosome_size
        self.bit_size = bit_size
        self.max_conflicts = max_conflicts

    def __str__(self):
        result = []
        sequence = list(self.__bitsToInts(self.sequence, 3))
        for i in range(self.size):
            line = []
            for j in range(self.size):
                if sequence[i] == j:
                    line.append('Q')
                else:
                    line.append('+')
            line.append('\n')
            result.append(''.join(line))
        return ''.join(result)

    def __bitsToInts(self, bits, dim):
        i, count = 0, 0
        for bit in bits:
            i = (i << 1) | bit
            count += 1
            if count == 3:
                count = 0
                yield i
                i = 0

    def copy(self):
        new_chromosome = Chromosome(self.size, self.bit_size, self.max_conflicts)
        new_chromosome.fitness = self.fitness
        new_chromosome.sequence = bitarray(self.sequence)
        return new_chromosome

    def calculateFitness(self):
        sequence = list(self.__bitsToInts(self.sequence, 3))

        fitness = self.max_conflicts - abs(self.size - len(np.unique(sequence)))
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if abs(sequence[j] - sequence[i]) == j - i:
                    fitness -= 1

        self.fitness = fitness / (self.max_conflicts*1.0)

    def generateSequence(self):
        positions = list(np.random.random_integers(0, self.size - 1, self.size))
        self.sequence = bitarray()
        for pos in positions:
            self.sequence.extend(bin(pos)[2:].zfill(3))

    def crossover(self, other, cross_point):
        for i in range(cross_point * 3, self.bit_size):
            self.sequence[i], other.sequence[i] = other.sequence[i], self.sequence[i]
        self.calculateFitness()
        other.calculateFitness()

        return self, other

    def mutate(self):
        position = np.random.random_integers(self.bit_size - 1)
        self.sequence[position] = ~self.sequence[position]
        self.calculateFitness()

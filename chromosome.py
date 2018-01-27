import random
import copy
import helper as h


class Chromosome:
    def __init__(self, sequence, queen_num, size, max_conflicts):
        if sequence is not None:
            self.sequence = sequence
        else:
            self.sequence = list([bool(random.getrandbits(1)) for _ in range(size)])

        self.size = size
        self.encoding_dim = int(size/queen_num)
        self.queen_num = queen_num
        self.max_conflicts = max_conflicts
        self.changed = True
        self.__fitness__ = 0

    def __str__(self):
        result = []
        int_presentation = h.bit_to_int(self.sequence, self.encoding_dim)

        for i in range(self.queen_num):
            line = []
            for j in range(self.queen_num):
                if int_presentation[i] == j:
                    line.append('Q')
                else:
                    line.append('+')
            line.append('\n')
            result.append(''.join(line))
        return ''.join(result)

    def copy(self):
        return copy.deepcopy(self)

    @property
    def fitness(self):
        if not self.changed:
            return self.__fitness__

        int_presentation = h.bit_to_int(self.sequence, self.encoding_dim)

        fitness = self.max_conflicts - self.queen_num + len(set(int_presentation))
        for i in range(self.queen_num):
            for j in range(i + 1, self.queen_num):
                if abs(int_presentation[j] - int_presentation[i]) == j - i:
                    fitness -= 1

        self.changed = False
        self.__fitness__ = fitness / (self.max_conflicts*1.0)
        return self.__fitness__

    def crossover(self, other, cross_point):
        for i in range(cross_point , self.size):
            self.sequence[i], other.sequence[i] = other.sequence[i], self.sequence[i]

        self.changed = True
        other.changed = True

        return self, other

    def mutate(self):
        position = random.randint(0, self.size - 1)
        self.sequence[position] = not self.sequence[position]
        self.changed = True

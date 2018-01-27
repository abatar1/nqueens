class GeneticSimulator:
    def __init__(self, population, cross_prob, mutation_prob):
        self.population = population
        self.population_size = len(population.chromosomes)
        self.cross_prob = cross_prob
        self.mutation_prob = mutation_prob
        self.epoch_num = 0
        self.best_result = self.population.best_result

    def step(self):
        parents_population = self.population.selection()
        children_population = []

        for i in range(int(self.population_size / 2)):
            children = self.population.crossover(parents_population, self.cross_prob)
            if children is not None:
                mutated_children = self.population.mutate(children, self.mutation_prob)
                children_population.extend(mutated_children)
        self.population.reduction(children_population)

        if self.population.best_result.fitness > self.best_result.fitness:
            self.best_result = self.population.best_result

    def is_end(self, max_epochs, min_fitness):
        if max_epochs is not None and self.epoch_num + 1 > max_epochs:
            return True

        if self.population.is_final(min_fitness):
            return True

        self.epoch_num += 1
        return False

    @property
    def state(self):
        return 'fitness: ' + str(self.population.best_result.fitness) \
               + '. epoch: ' + str(self.epoch_num)

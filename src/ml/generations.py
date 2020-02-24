from generation import Generation
from network import Network


class Generations(object):

    def __init__(self, network_layers, num_per_gen, num_children, elitism, mutation_rate, mutation_range, score_sort, random_behavior):
        self.network_layers = network_layers
        self.generations = []
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.score_sort = score_sort
        self.num_per_gen = num_per_gen
        self.random_behavior = random_behavior
        self.num_children = num_children
        self.cur_gen = Generation(self.num_per_gen, self.num_children,
                                  self.elitism, self.mutation_rate,
                                  self.mutation_range, self.score_sort,
                                  self.random_behavior)

    def first_generation(self):
        out = []
        for i in range(self.num_per_gen):
            nn = Network()
            nn.perceptron_generation(self.network_layers[0], self.network_layers[1], self.network_layers[2])
            out.append(nn.get_save())

        self.generations.append(Generation(self.num_per_gen, self.num_children,
                                           self.elitism, self.mutation_rate,
                                           self.mutation_range, self.score_sort,
                                           self.random_behavior)
                                )
        return out

    def next_generation(self):
        if len(self.generations) == 0:
            return self.first_generation()

        gen = self.generations[-1].generate_next_generation()
        self.generations.append(Generation(self.num_per_gen, self.num_children,
                                           self.elitism, self.mutation_rate,
                                           self.mutation_range, self.score_sort,
                                           self.random_behavior)
                                )
        return gen

    def add_genome(self, g):
        if len(self.generations) == 0:
            return False
        return self.generations[-1].add_genome(g)

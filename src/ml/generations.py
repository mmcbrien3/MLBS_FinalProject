from generation import Generation
from network import Network

network_layers = [1, [], 1]


class Generations(object):

    def __init__(self):
        self.generations = []
        self.num_per_gen = 30
        self.cur_gen = Generation()

    def first_generation(self):
        out = []
        for i in range(self.num_per_gen):
            nn = Network()
            nn.perceptron_generation(network_layers[0], network_layers[1], network_layers[2])
            out.append(nn.get_save())

        self.generations.append(Generation())
        return out

    def next_generation(self):
        if len(self.generations) == 0:
            return self.first_generation()

        gen = self.generations[-1].generate_next_generation()
        self.generations.append(Generation())
        return gen

    def add_genome(self, g):
        if len(self.generations) == 0:
            return False
        return self.generations[-1].add_genome(g)

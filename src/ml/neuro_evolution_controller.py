import os
from src.ml.generations import Generations
from src.ml.base_controller import BaseController


class NeuroEvolutionController(BaseController):

    best_ever_file = os.path.join(os.getcwd(), "best_ever_neuroevolution.txt")
    best_per_gen_file = os.path.join(os.getcwd(), "best_per_gen_neuroevolution.txt")
    best_per_gen_pickle_folder = os.path.join(os.getcwd(), "neural_nets")

    def __init__(self, num_per_gen=30, num_children=1, elitism=0.2,
                 mutation_rate=0.5, mutation_range=0.5, random_behavior=0.1,
                 network_layers=(8, (8, 8, 8, 8), 4)):
        super().__init__()
        self.num_per_gen = num_per_gen
        self.num_children = num_children
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.random_behavior = random_behavior

        self.network_layers = network_layers

        self.generations = Generations(Generations.NE_GENERATION_TYPE, self.network_layers, self.num_per_gen,
                                       self.num_children, self.elitism,
                                       self.mutation_rate, self.mutation_range,
                                       self.score_sort, self.random_behavior)

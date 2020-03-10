import os
from src.ml.generations import Generations
from src.ml.base_controller import BaseController


class NeuroEvolutionController(BaseController):

    best_ever_file = os.path.join(os.getcwd(), "best_ever_neuroevolution.txt")
    best_per_gen_file = os.path.join(os.getcwd(), "best_per_gen_neuroevolution.txt")
    best_per_gen_pickle_folder = os.path.join(os.getcwd(), "neural_nets")

    def __init__(self):
        super().__init__()
        self.num_per_gen = 30
        self.num_children = 1
        self.elitism = 0.2
        self.mutation_rate = 0.2
        self.mutation_range = 0.5
        self.score_sort = -1
        self.random_behavior = 0.1

        self.network_layers = (8, (8, 8, 8, 8), 4)

        self.generations = Generations(Generations.NE_GENERATION_TYPE, self.network_layers, self.num_per_gen,
                                       self.num_children, self.elitism,
                                       self.mutation_rate, self.mutation_range,
                                       self.score_sort, self.random_behavior)

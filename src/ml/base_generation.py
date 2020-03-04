import random
import numpy as np


class BaseGeneration:

    def __init__(self):
        self.genomes = None

    def add_genome(self, genome):
        pass

    def fuck(self, parent_one, parent_two, num_children):
        pass

    def generate_next_generation(self):
        pass

    def _calc_percentiles(self):
        tot_score = sum([g.score for g in self.genomes])
        tot_score = 0.1 if tot_score == 0 else tot_score
        percentiles = []
        tot_percentile = 0
        for g in self.genomes:
            perc = g.score / tot_score
            percentiles.append(perc + tot_percentile)
            tot_percentile += perc
        return percentiles

    def _select_parents(self, percentiles):
        p1 = None
        p2 = None
        p1_perc = random.random()
        p2_perc = random.random()
        count = 0
        prev_perc = 0
        for perc in percentiles:
            if perc >= p1_perc > prev_perc:
                p1 = self.genomes[count]
            if perc >= p2_perc > prev_perc:
                p2 = self.genomes[count]
            if p1 and p2:
                if p1 is p2:
                    p2 = np.random.choice(self.genomes)
                return [p1, p2]
            prev_perc = perc
            count += 1

        return [np.random.choice(self.genomes), np.random.choice(self.genomes)]

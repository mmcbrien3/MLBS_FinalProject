import random
import copy
from neuron import Neuron


class Generation(object):

    def __init__(self, num_per_gen, num_children, elitism, mutation_rate, mutation_range, score_sort, random_behavior):
        self.genomes = []
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.score_sort = score_sort
        self.num_per_gen = num_per_gen
        self.random_behavior = random_behavior
        self.num_children = num_children

    def add_genome(self, genome):
        count = 0
        while count < len(self.genomes):
            if self.score_sort < 0:
                if genome.score > self.genomes[count].score:
                    break
            else:
                if genome.score < self.genomes[count].score:
                    break
            count += 1

        self.genomes.insert(count, genome)

    def fuck(self, g1, g2, num_children):
        datas = []
        for n in range(num_children):
            data = copy.deepcopy(g1)
            for i in range(len(g2.network["weights"])):
                if random.random() <= 0.5:
                    data.network["weights"][i] = g2.network["weights"][i]

            for i in range(len(data.network["weights"])):
                if random.random() < self.mutation_rate:
                    data.network["weights"][i] += random.random() * self.mutation_range * 2 - self.mutation_range

            datas.append(data)

        return datas

    def generate_next_generation(self):
        nexts = []
        for i in range(round(self.elitism * self.num_per_gen)):
            if len(nexts) < self.num_per_gen:
                nexts.append(copy.deepcopy(self.genomes[i].network))

        for i in range(round(self.random_behavior * self.num_per_gen)):
            n = copy.deepcopy(self.genomes[0].network)
            for k in range(len(n["weights"])):
                n["weights"][k] = Neuron.random_clamped()
            if len(nexts) < self.num_per_gen:
                nexts.append(n)

        maximum = 0
        percentiles = self.calc_percentiles()
        while True:
            parents = self.select_parents(percentiles)
            children = self.fuck(parents[0], parents[1], self.num_children)
            for c in children:
                nexts.append(c.network)
                if len(nexts) >= self.num_per_gen:
                    return nexts

    def calc_percentiles(self):
        tot_score = sum([g.score for g in self.genomes])
        percentiles = []
        tot_percentile = 0
        for g in self.genomes:
            perc = g.score / tot_score
            percentiles.append(perc + tot_percentile)
            tot_percentile += perc
        return percentiles

    def select_parents(self, percentiles):
        p1 = None
        p2 = None
        p1_perc = random.random()
        p2_perc = random.random()
        count = 0
        prev_perc = 0
        for perc in percentiles:
            if p1_perc <= perc and p1_perc > prev_perc:
                p1 = self.genomes[count]
            if p2_perc <= perc and p2_perc > prev_perc:
                p2 = self.genomes[count]
            if p1 and p2:
                return [p1, p2]
            prev_perc = perc
            count += 1
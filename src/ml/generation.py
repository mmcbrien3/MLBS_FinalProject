import random
import copy
from neuron import Neuron

num_per_gen = 30
elitism = 0.2
random_behavior = 0.2
mutation_rate = 0.1
mutation_range = 0.5
low_historic = False
score_sort = -1
num_child = 1

class Generation(object):
    def __init__(self):
        self.genomes = []

    def add_genome(self, genome):
        count = 0
        while count < len(self.genomes):
            if score_sort < 0:
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
                if random.random() < mutation_rate:
                    data.network["weights"][i] += random.random() * mutation_range * 2 - mutation_range

            datas.append(data)

        return datas

    def generate_next_generation(self):
        nexts = []
        for i in range(round(elitism*num_per_gen)):
            if len(nexts) < num_per_gen:
                nexts.append(copy.deepcopy(self.genomes[i].network))

        for i in range(round(random_behavior*num_per_gen)):
            n = copy.deepcopy(self.genomes[0].network)
            for k in range(len(n["weights"])):
                n["weights"][k] = Neuron.random_clamped()
            if len(nexts) < num_per_gen:
                nexts.append(n)

        maximum = 0
        percentiles = self.calc_percentiles()
        while True:
            parents = self.select_parents(percentiles)
            children = self.fuck(parents[0], parents[1], num_child)
            for c in children:
                nexts.append(c.network)
                if len(nexts) >= num_per_gen:
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
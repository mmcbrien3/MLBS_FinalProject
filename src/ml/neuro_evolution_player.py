import math, random, copy, os
from generations import Generations
from network import Network
from genome import Genome


historic = 0

class NeuroEvolutionPlayer(object):

    best_ever_file = os.path.join(os.getcwd(), "best_ever_neuroevolution.txt")
    best_per_gen_file = os.path.join(os.getcwd(), "best_per_gen_neuroevolution.txt")

    def __init__(self):
        if os.path.isfile(self.best_ever_file):
            os.remove(self.best_ever_file)
        if os.path.isfile(self.best_per_gen_file):
            os.remove(self.best_per_gen_file)
        try:
            os.remove(self.best_per_gen_file)
        except:
            pass
        self.num_per_gen = 30
        self.max_gen = 500
        self.cur_gen = 0
        self.cur_bird = None
        self.best_score_ever = -1

        self.generations = Generations()

    def restart(self):
        self.generations = Generations()

    def increment_gen(self):
        self.save_best_score()
        self.cur_gen = self.cur_gen + 1
        self.cur_bird = None

        networks = []
        print("Creating Gen #%d" % self.cur_gen)
        if self.cur_gen == 1:
            networks = self.generations.first_generation()
        else:
            networks = self.generations.next_generation()

        nns = []
        for i in range(len(networks)):
            nn = Network()
            nn.set_save(networks[i])
            nns.append(nn)

        if not historic == -1:
            if len(self.generations.generations) > historic + 1:
                self.generations.generations = self.generations.generations[len(self.generations.generations) - (historic+1):]

        return nns

    def network_score(self, network, score):
        self.generations.add_genome(Genome(score, network.get_save()))

    def make_decision(self, stimuli, nn):
        score = nn.compute(stimuli)
        if score[0] > 0.5:
            return "SPACE"
        return "do nothing"

    def save_best_score(self, frame_score = None, count = None):
        if len(self.generations.generations) == 0:
            return
        best_score_in_gen = -1
        best_in_gen = None
        if not frame_score:
            for g in self.generations.generations[0].genomes:
                if g.score > best_score_in_gen:
                    best_in_gen = g
                    best_score_in_gen = g.score
        else:
            best_in_gen = self.generations.generations[0].genomes[count]
            best_score_in_gen = frame_score

        fhandler = open(self.best_per_gen_file, "a")
        fhandler.writelines("Gen #%d scored %f pts: " % (self.cur_gen, best_in_gen.score) + str(best_in_gen.network) + "\n")
        fhandler.close()

        if best_score_in_gen > self.best_score_ever:
            fhandler = open(self.best_ever_file, "w")
            fhandler.writelines("Gen #%d scored %f pts: " % (self.cur_gen, best_in_gen.score) + str(best_in_gen.network) + "\n")
            fhandler.close()
            self.best_score_ever = best_score_in_gen

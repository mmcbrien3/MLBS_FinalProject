from src.ml.genome import Genome
from src.ml.network import Network
import os
import pickle

class BaseController(object):

    best_ever_file = "base_controller_best_ever.txt"
    best_per_gen_file = "base_controller_best_per_gen.txt"

    def __init__(self):
        if os.path.isfile(self.best_ever_file):
            os.remove(self.best_ever_file)
        if os.path.isfile(self.best_per_gen_file):
            os.remove(self.best_per_gen_file)
        self.historic = 0
        self.cur_gen = 0
        self.best_score_ever = -1
        self.score_sort = -1

        self.generations = None

    def increment_gen(self):
        self.save_best_score()
        self.cur_gen = self.cur_gen + 1

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

        if not self.historic == -1:
            if len(self.generations.generations) > self.historic + 1:
                self.generations.generations = self.generations.generations[
                                               len(self.generations.generations) - (self.historic + 1):]

        return nns

    def submit_network_and_score(self, network, score):
        self.generations.add_genome(Genome(score, network.get_save()))

    def save_best_score(self, frame_score=None, count=None):
        if len(self.generations.generations) == 0:
            return
        best_score_in_gen = self.generations.generations[0].genomes[0].score
        best_in_gen = self.generations.generations[0].genomes[0]
        if not frame_score:
            for g in self.generations.generations[0].genomes:
                if g.score > best_score_in_gen:
                    best_in_gen = g
                    best_score_in_gen = g.score
        else:
            best_in_gen = self.generations.generations[0].genomes[count]
            best_score_in_gen = frame_score

        fhandler = open(self.best_per_gen_file, "a")
        fhandler.writelines(
            "Gen #%d scored %f pts: " % (self.cur_gen, best_in_gen.score) + str(best_in_gen.network) + "\n")
        fhandler.close()

        with open(os.path.join(self.best_per_gen_pickle_folder, "Gen_{}".format(self.cur_gen)), "wb") as file:
            pickle.dump(best_in_gen.network, file)

        if best_score_in_gen > self.best_score_ever:
            fhandler = open(self.best_ever_file, "w")
            fhandler.writelines(
                "Gen #%d scored %f pts: " % (self.cur_gen, best_in_gen.score) + str(best_in_gen.network) + "\n")
            fhandler.close()
            self.best_score_ever = best_score_in_gen
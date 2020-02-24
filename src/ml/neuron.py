import random


class Neuron(object):
    def __init__(self):
        self.value = 0
        self.weights = []

    def populate(self, num):
        self.weights = []
        for i in range(num):
            self.weights.append(self.random_clamped())

    @staticmethod
    def random_clamped():
        return random.random() * 2 - 1

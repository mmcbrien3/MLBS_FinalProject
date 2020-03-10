from src.ml.neuron import Neuron


class Layer(object):

    def __init__(self, idx=0):
        self.idx = idx
        self.neurons = []

    def populate(self, num_neurons, num_inputs):
        self.neurons = []
        for i in range(num_neurons):
            n = Neuron()
            n.populate(num_inputs)
            self.neurons.append(n)

from src.ml.layer import Layer
from scipy.stats import logistic
import numpy as np
import pygame as pg

class Network(object):

    LEFT_INPUTS = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
    RIGHT_INPUTS = [pg.K_i, pg.K_j, pg.K_k, pg.K_l]

    def __init__(self):
        self.layers = []

    def perceptron_generation(self, num_input_neurons, hiddens, num_outputs):
        index = 0
        num_prev_neurons = 0
        layer = Layer(index)
        layer.populate(num_input_neurons, num_prev_neurons)
        num_prev_neurons = num_input_neurons
        self.layers.append(layer)
        index += 1
        for h in hiddens:
            layer = Layer(index)
            layer.populate(h, num_prev_neurons)
            num_prev_neurons = h
            self.layers.append(layer)
            index += 1
        layer = Layer(index)
        layer.populate(num_outputs, num_prev_neurons)
        self.layers.append(layer)

    def get_save(self):
        data = {"neurons": [], "weights": []}

        for i in range(len(self.layers)):
            data["neurons"].append(len(self.layers[i].neurons))
            for j in range(len(self.layers[i].neurons)):
                for k in range(len(self.layers[i].neurons[j].weights)):
                    data["weights"].append(self.layers[i].neurons[j].weights[k])

        return data

    def set_save(self, save):
        prev_neurons = 0
        index = 0
        index_weights = 0
        self.layers = []
        for i in range(len(save["neurons"])):
            layer = Layer(index)
            layer.populate(save["neurons"][i], prev_neurons)
            for j in range(len(layer.neurons)):
                for k in range(len(layer.neurons[j].weights)):
                    layer.neurons[j].weights[k] = save["weights"][index_weights]
                    index_weights +=1
            prev_neurons = save["neurons"][i]
            index += 1
            self.layers.append(layer)

    def compute(self, inputs):

        for i in range(len(inputs)):
            if self.layers[0] and self.layers[0].neurons[i]:
                self.layers[0].neurons[i].value = inputs[i]

        prev_layer = self.layers[0]
        for i in range(1, len(self.layers)):
            for j in range(len(self.layers[i].neurons)):
                sum = 0
                for k in range(len(prev_layer.neurons)): # TODO: optimize with numpy
                    sum += prev_layer.neurons[k].value * self.layers[i].neurons[j].weights[k]
                self.layers[i].neurons[j].value = self.activation(sum)
            prev_layer = self.layers[i]

        out = []
        last_layer = self.layers[-1]
        for i in range(len(last_layer.neurons)):
            out.append(last_layer.neurons[i].value)

        return out

    def activation(self, a):
        return logistic.cdf(a)

    def convert_output_to_keyboard_input(self, nn_output, side):
        if side == "LEFT":
            return self.LEFT_INPUTS[np.argmax(nn_output)]
        else:
            return self.RIGHT_INPUTS[np.argmax(nn_output)]

if __name__ == "__main__":
    n = Network()
    d = {}
    d[n] = 3
    print(d)
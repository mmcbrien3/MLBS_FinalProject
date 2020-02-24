from layer import Layer
from scipy.stats import logistic


class Network(object):

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

        for i in range(len(inputs[0])):
            if self.layers[0] and self.layers[0].neurons[i]:
                self.layers[0].neurons[i].value = inputs[0][i]

        prev_layer = self.layers[0]
        for i in range(1, len(self.layers)):
            for j in range(len(self.layers[i].neurons)):
                sum = 0
                for k in range(len(prev_layer.neurons)):
                    sum += prev_layer.neurons[k].value * self.layers[i].neurons[j].weights[k]
                self.layers[i].neurons[j].value = self.activation(sum)
            prev_layer = self.layers[i]

        out = []
        last_layer = self.layers[-1]
        for i in range(len(last_layer.neurons)):
            out.append(last_layer.neurons[i].value)

        return out

    def activation(a):
        return logistic.cdf(a)
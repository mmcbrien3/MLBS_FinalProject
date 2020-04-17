import src.ml.network
import jsonpickle


class NEATNetwork(src.ml.network.Network):

    def __init__(self):
        super().__init__()
        self.network = None
        self.genome = None

    def compute(self, inputs):
        return self.network.activate(inputs)

    def set_save(self, save):
        self.network = jsonpickle.loads(save)

    def get_save(self):
        return jsonpickle.dumps(self.network)
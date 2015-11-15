from helper import *
import theano
from helper import *
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np

srng = RandomStreams()

class Layer:
    def __init__(self, input, output, activation):
        self.input = input
        self.output = output
        self.activation_function = activation

class ANN:
    def __init__(self):
        pass


    def create_layers(self, layer_sizes, layer_activations):
    '''
    Note:
        Both lists must be the same length.

    Args:
        layer_sizes: List of sizes for the layers, including input and output.
            Format: [10, 20, 30, 40]
        layer_activations: List of activation functions for each layer.
            Format: ["rect", "soft", "sig"]

    Attributes:
        layers:
    '''

    assert len(layer_sizes) == len(layer_activations)

    self.layers = []
    input = 784

    for size, activation in zip(layer_sizes, layer_activations):
        layer = None
        if activation == "rect":
            layer = Layer(input, size, rectify)
        elif activation == "soft":
            layer = Layer(input, size, softmax)

        input = size
        self.layers.append(layer)



    def noise_removal(self, flatten_input_matrix, p=0.):
        if p > 0:
            retain_prob = 1 - p
            X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
            X /= retain_prob
        return X

    # Activation function
    @staticmethod
    def rectify(flatten_input_matrix):
        return T.maximum(flatten_input_matrix, 0.)

    @staticmethod
    def softmax(flatten_input_matrix):
        e_x = T.exp(flatten_input_matrix - flatten_input_matrix.max(axis=1).dimshuffle(0, 'x'))
        return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')


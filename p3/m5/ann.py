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

    @staticmethod
    def floatX(X):
        return np.asarray(X, dtype=theano.config.floatX)

    def create_shape(self):
        self.shape = theano.shared(self.floatX(np.random.randn(self.input, self.output) * 0.01))

class ANN:
    def __init__(self):
        self.training_images, self.training_labels = load_all_flat_cases(type='training')
        self.test_images, self.test_labels = load_all_flat_cases(type='testing')
        self.grayscale()
        self.convert_number_to_array()

    def grayscale(self):
        training = []
        for img in self.training_images:
            img = np.asarray(img)
            training.append(img/255)
        self.training_images = training

        test = []
        for img in self.test_images:
            img = np.asarray(img)
            test.append(img/255)
        self.test_images = test

    def convert_number_to_array(self):
        training = []
        for label in self.training_labels:
            arr = np.zeros(10)
            arr.put(label, 1)
            training.append(arr)
        self.training_labels = training

        test = []
        for label in self.test_labels:
            arr = np.zeros(10)
            arr.put(label, 1)
            test.append(arr)
        self.test_labels = test


    # Activation function
    @staticmethod
    def rectify(flatten_input_matrix):
        return T.maximum(flatten_input_matrix, 0.)

    @staticmethod
    def softmax(flatten_input_matrix):
        e_x = T.exp(flatten_input_matrix - flatten_input_matrix.max(axis=1).dimshuffle(0, 'x'))
        return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

    @staticmethod
    def sigmoid(flatten_input_matrix):
        return T.nnet.sigmoid(flatten_input_matrix)

    @staticmethod
    def RMSprop(cost, params, lr=0.001, rho=0.9, epsilon=1e-6):
        grads = T.grad(cost=cost, wrt=params)
        updates = []
        for p, g in zip(params, grads):
            acc = theano.shared(p.get_value() * 0.)
            acc_new = rho * acc + (1 - rho) * g ** 2
            gradient_scaling = T.sqrt(acc_new + epsilon)
            g = g / gradient_scaling
            updates.append((acc, acc_new))
            updates.append((p, p - lr * g))
        return updates


    def create_layers(self, layer_sizes, layer_activations):
        '''
        Note:
            Both lists must be the same length.
q
        Args:
            layer_sizes: List of sizes for the layers, including input and output.
                Format: [10, 20, 30, 40]
            layer_activations: List of activation functions for each layer.
                Format: ["rect", "soft", "sig"]

        Attributes:
            layers:
        '''

        assert len(layer_sizes)-1 == len(layer_activations)

        self.layers = []
        input = layer_sizes.pop(0)

        for size, activation in zip(layer_sizes, layer_activations):
            layer = None
            if activation == 'rect':
                layer = Layer(input, size, self.rectify)
            elif activation == 'soft':
                layer = Layer(input, size, self.softmax)
            elif activation == 'sig':
                layer = Layer(input, size, self.sigmoid)

            print('created layer with: ({}, {}), {}'.format(input, size, activation))
            input = size
            layer.create_shape()
            self.layers.append(layer)

    def model(self, X):
        #l = self.noise_removal(X, drop_input)

        l = X
        for layer in self.layers:
            l = layer.activation_function(T.dot(l, layer.shape))

        return l


if __name__ == "__main__":


    scenario_sizes = [
        [784, 100, 10],
        [784, 300, 10],
        [784, 625, 100, 10],
        [784, 625, 625, 10],
        [784, 625, 300, 100, 10],
    ]

    scenario_act = [
        ['rect', 'soft'],
        ['rect', 'soft'],
        ['rect', 'rect', 'soft'],
        ['rect', 'rect', 'soft'],
        ['rect', 'sig', 'sig', 'soft'],
    ]

    for sizes, activations in zip(scenario_sizes, scenario_act):
        ann = ANN()

        X = T.fmatrix()
        Y = T.fmatrix()

        layer_sizes = sizes
        layer_activations = activations

        ann.create_layers(layer_sizes, layer_activations)

        pyx = ann.model(X)

        yx = T.argmax(pyx, axis=1)

        # SOMETHING CAN BE WRONG HERE
        output = ann.layers[-1].shape
        cost = T.sum((Y-pyx)**2, acc_dtype=theano.config.floatX)
        # cost = T.mean(T.nnet.categorical_crossentropy(X, Y))
        params = [x.shape for x in ann.layers]
        updates = ann.RMSprop(cost, params, lr=0.001)

        train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        predict = theano.function(inputs=[X], outputs=yx, allow_input_downcast=True)

        tri = ann.training_images
        trl = ann.training_labels

        for i in range(10):
            for start, end in zip(list(range(0, len(tri), 128)), list(range(128, len(tri), 128))):
                cost = train(tri[start:end], trl[start:end])
            print(np.mean(np.argmax(ann.test_labels, axis=1) == predict(ann.test_images)))

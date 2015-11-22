import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from dump import *

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
    def __init__(self, trains, learningrate, layer_sizes, layer_activations, notation, batchsize):
        print(theano.config.allow_gc)
        if notation == "original":
            self.boards, self.moves = load_all('dump.pkl')
        else:
            self.boards, self.moves = transform_all_boards('dump.pkl')


        self.X = T.fmatrix()
        self.Y = T.fmatrix()

        self.create_layers(layer_sizes, layer_activations)

        self.pyx = self.model(self.X)

        self.yx = T.argmax(self.pyx, axis=1)

        # SOMETHING CAN BE WRONG HERE
        self.output = self.layers[-1].shape
        self.cost = T.sum((self.Y-self.pyx)**2, acc_dtype=theano.config.floatX)
        # cost = T.mean(T.nnet.categorical_crossentropy(X, Y))
        self.params = [x.shape for x in self.layers]
        self.updates = self.RMSprop(self.cost, self.params, lr=learningrate)

        self.train = theano.function(inputs=[self.X, self.Y], outputs=self.cost, updates=self.updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[self.X], outputs=self.pyx, allow_input_downcast=True)

        tri = self.boards
        trl = self.moves
        print(self.boards[1000])
        for i in range(trains):
            print(i)
            for start, end in zip(list(range(0, len(tri), batchsize)), list(range(batchsize, len(tri), batchsize))):
                self.cost = self.train(tri[start:end], trl[start:end])
            print(np.mean(np.argmax(trl, axis=1) == np.argmax(self.predict(tri), axis=1)))
            print(self.predict([tri[1000]]))


    def convert_number_to_array(self, data):
        converted_data = []
        for label in data:
            arr = np.zeros(10, dtype=theano.config.floatX)
            print(label)
            arr.put(np.float32(label), np.float32(1))
            converted_data.append(arr)

        return converted_data


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
    def hardsig(flatten_input_matrix):
        return T.nnet.hard_sigmoid(flatten_input_matrix)

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
            elif activation == 'hard':
                layer = Layer(input, size, self.hardsig)

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


    def go(self, board=None):
        if board != None:
            board = np.asarray(board, dtype=theano.config.floatX).flatten()
            return self.predict([board])

        predictions = self.predict(self.boards)
        print(len(predictions))
        #return predictions.tolist()
        print(predictions)
        print(np.mean(np.argmax(self.moves, axis=1) == predictions))



if __name__ == "__main__":
    pass


    #scenario_sizes = [
    #    [16, 8, 4],
    #]

    #scenario_act = [
    #    ['rect', 'soft'],
    #]

    #ann = ANN(scenario_sizes[0], scenario_act[0])
    #ann.go()

    #minor_demo(ann)

    #for sizes, activations in zip(scenario_sizes, scenario_act):
    #    ann = ANN(sizes, activations)


    #    tri = ann.training_images
    #    trl = ann.training_labels

    #    ann.test_images, ann.test_labels = load_flat_cases_as_sets('demo_prep')
    #    ann.grayscale()
    #    ann.test_labels = ann.convert_number_to_array(ann.test_labels)

    #    for i in range(20):
    #        for start, end in zip(list(range(0, len(tri), 128)), list(range(128, len(tri), 128))):
    #            ann.cost = ann.train(tri[start:end], trl[start:end])
    #        print(np.mean(np.argmax(ann.test_labels, axis=1) == ann.predict(ann.test_images)))
    #        print(ann.predict(ann.test_images))

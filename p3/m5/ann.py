import theano
from mnist_basics import *
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
    def __init__(self, layer_sizes, layer_activations):
        self.training_images, self.training_labels = load_all_flat_cases(type='training')
        self.test_images, self.test_labels = load_all_flat_cases(type='testing')
        self.grayscale()
        self.test_labels = self.convert_number_to_array(self.test_labels)
        self.training_labels = self.convert_number_to_array(self.training_labels)


        X = T.fmatrix()
        Y = T.fmatrix()

        def floatX(X):
            return np.asarray(X, dtype=theano.config.floatX)

        def init_weights(shape):
            return theano.shared(floatX(np.random.randn(*shape) * 0.01))

        w_h = init_weights((784, 625))
        w_h2 = init_weights((625, 625))
        w_o = init_weights((625, 10))

        self.create_layers(layer_sizes, layer_activations)

        noise_py_x = self.model(X, 0.2, 0.5)
        py_x = self.model(X, 0., 0.)
        y_x = T.argmax(py_x, axis=1)

        cost = T.mean(T.nnet.categorical_crossentropy(noise_py_x, Y))
        params = [w_h, w_h2, w_o]
        print(params)
        params = [x.shape for x in self.layers]
        print(params)

        updates = self.RMSprop(cost, params, lr=0.001)

        self.train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)

        tri = self.training_images
        trl = self.training_labels
        for i in range(5):
            for start, end in zip(list(range(0, len(tri), 128)), list(range(128, len(tri), 128))):
                cost = self.train(tri[start:end], trl[start:end])
                print(cost)
            print(np.mean(np.argmax(trl, axis=1) == self.predict(tri)))


    def grayscale(self):
        training = []
        for img in self.training_images:
            img = np.asarray(img, dtype=theano.config.floatX)
            training.append(img/255)
        self.training_images = training

        test = []
        for img in self.test_images:
            img = np.asarray(img, dtype=theano.config.floatX)
            test.append(img/255)
        self.test_images = test

    def convert_number_to_array(self, data):
        converted_data = []
        for label in data:
            arr = np.zeros(10, dtype=theano.config.floatX)
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
        Args:
            layer_sizes: List of sizes for the layers, including input and output.
                Format: [10, 20, 30, 40]
            layer_activations: List of activation functions for each layer.
                Format: ["rect", "soft", "sig"]

        Attributes:
            layers:
        '''

        assert len(layer_sizes) - 1 == len(layer_activations)

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


    def dropout(self, X, p):
        if p > 0:
            retain_prob = 1 - p
            X *= srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
            X /= retain_prob
        return X

    def model(self, X, input_dropout, hidden_dropout):
        #l = self.noise_removal(X, drop_input)

        X = self.dropout(X, input_dropout)
        l = X
        for layer in self.layers:
            l = layer.activation_function(T.dot(l, layer.shape))
            l = self.dropout(l, hidden_dropout)

        return l


    def blind_test(self, images):
        self.test_images = images
        self.grayscale()
        return self.go()

    def go(self):
        predictions = self.predict(self.test_images)
        print(len(predictions))
        return predictions.tolist()



if __name__ == "__main__":


    scenario_sizes = [
        #[784, 100, 10],
        #[784, 300, 10],
        #[784, 625, 100, 10],
        [784, 625, 625, 10],
        #[784, 620, 620, 10],
        #[784, 625, 300, 100, 10],
    ]

    scenario_act = [
        #['rect', 'soft'],
        #['rect', 'soft'],
        #['rect', 'rect', 'soft'],
        ['rect', 'rect', 'soft'],
        #['rect', 'rect', 'soft'],
        #['rect', 'sig', 'sig', 'soft'],
    ]

    ann = ANN(scenario_sizes[0], scenario_act[0])

    minor_demo(ann)

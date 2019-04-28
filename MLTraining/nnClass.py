from nn import *
import random
import math
import numpy as np


class ActivationFunction:
    def __init__(self, func, dfunc):
        self.func = np.vectorize(func)
        self.dfunc = np.vectorize(dfunc)


sigmoid = ActivationFunction(
    lambda x: 1/(1 + math.exp(-x)),
    lambda y: y * (1-y))

tanh = ActivationFunction(
    lambda x: math.tanh(x),
    lambda y: 1-(y*y)
)


class NeuralNetwork:
    def __init__(self, in_nodes, hid_nodes, out_nodes):
        self.input_nodes = in_nodes
        self.hidden_nodes = hid_nodes
        self.output_nodes = out_nodes

        self.weights_ih = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.weights_ho = np.random.rand(self.output_nodes, self.hidden_nodes)

        self.bias_h = np.random.rand(self.hidden_nodes, 1)
        self.bias_o = np.random.rand(self.output_nodes, 1)

        self.learning_rate = 0.01
        self.activation_function = tanh

    def setLearningRate(self, learning_rate):
        self.learning_rate = learning_rate

    def setActivationFunction(self, func):
        self.activation_function = func

    def predict(self, input):

        input = np.matrix(input).transpose()
        # output for each layer =
        # f(weights DOT inputs + biases)

        hidden = np.dot(self.weights_ih, input) + self.bias_h
        hidden = np.matrix(self.activation_function.func(hidden))

        output = np.dot(self.weights_ho, hidden) + self.bias_o
        output = np.matrix(self.activation_function.func(output))

        # print(output.shape)

        return output.tolist()

    def train(self, inputs_list, targets_list):
        # input = Matrix.fromList(input_list)
        input = np.matrix(inputs_list).transpose()
        hidden = np.dot(self.weights_ih, input) + self.bias_h
        # hidden.add(self.bias_h)
        hidden = np.matrix(self.activation_function.func(hidden))

        output = np.dot(self.weights_ho, hidden) + self.bias_o
        output = np.matrix(self.activation_function.func(output))
        # ------------------------------------------

        target = np.matrix(targets_list)

        # whats the output error
        output_errors = target - output

        # gradient of output
        gradient = np.matrix(self.activation_function.dfunc(output))
        gradient *= output_errors
        gradient *= self.learning_rate

        # how much to change output weights and biases
        weights_ho_deltas = np.dot(gradient, hidden.getT())
        # print(weights_ho_deltas)
        self.weights_ho += weights_ho_deltas
        self.bias_o += gradient

        # whats the error of the hidden layer
        hidden_error = np.dot(np.matrix(self.weights_ho).getT(), output_errors)

        # gradient of hidden
        hidden_gradient = self.activation_function.dfunc(hidden)
        hidden_gradient = np.multiply(hidden_gradient, hidden_error)
        hidden_gradient *= self.learning_rate

        # how much to change the hidden weights and biases
        weights_ih_deltas = np.dot(hidden_gradient, input.getT())
        self.weights_ih += weights_ih_deltas
        self.bias_h += hidden_gradient

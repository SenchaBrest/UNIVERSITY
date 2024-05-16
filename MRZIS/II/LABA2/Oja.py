import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler


class Autoencoder:
    def __init__(self, input_neuron, encoding_neuron, learning_rate):
        self.input_neuron = input_neuron
        self.encoding_neuron = encoding_neuron
        self.learning_rate = learning_rate

        self.weights_input_encoding = np.random.rand(input_neuron, encoding_neuron)
        self.weights_encoding_input = np.random.rand(encoding_neuron, input_neuron)
        self.bias_encoding = np.random.rand(1, encoding_neuron)
        self.bias_input = np.random.rand(1, input_neuron)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def encode(self, inputs):
        self.encoding_layer_input = np.dot(inputs, self.weights_input_encoding) + self.bias_encoding
        self.encoding_layer_output = self.sigmoid(self.encoding_layer_input)

    def decode(self, encoding_output):
        self.input_layer_input = np.dot(encoding_output, self.weights_encoding_input) + self.bias_input
        self.input_layer_output = self.sigmoid(self.input_layer_input)

    def backward_pass(self, inputs):
        encoding_error = inputs - self.input_layer_output
        encoding_delta = encoding_error * self.sigmoid_derivative(self.input_layer_output)

        self.weights_encoding_input += self.learning_rate * np.dot(self.encoding_layer_output.T, encoding_delta) / \
                                       inputs.shape[0]
        self.bias_input += self.learning_rate * np.mean(encoding_delta, axis=0, keepdims=True)

        decoding_error = encoding_delta.dot(self.weights_encoding_input.T)
        decoding_delta = decoding_error * self.sigmoid_derivative(self.encoding_layer_output)

        for i in range(self.encoding_neuron):
            delta_w = self.learning_rate * (self.encoding_layer_output[:, i][:, np.newaxis] * (
                        inputs - self.encoding_layer_output[:, i][:, np.newaxis] * self.weights_input_encoding[:,
                                                                                   i])).mean(axis=0)
            self.weights_input_encoding[:, i] += delta_w

        self.bias_encoding += self.learning_rate * np.mean(decoding_delta, axis=0, keepdims=True)

        mse = np.mean((inputs - self.input_layer_output) ** 2)
        self.errors.append(mse)

    def train(self, inputs, epochs=10):
        self.errors = []
        for _ in range(epochs):
            self.encode(inputs)
            self.decode(self.encoding_layer_output)
            self.backward_pass(inputs)

    def encode_data(self, inputs_data):
        self.encode(inputs_data)
        return self.encoding_layer_output

    def decode_data(self, encoded_data):
        self.decode(encoded_data)
        return self.input_layer_output


if __name__ == "__main__":
    data = pd.read_csv("/home/senya/UNIVERSITY/MRZIS/II/LABA2/Seed_Data.csv", header=None)
    X = data.iloc[:, :-1].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    autoencoder = Autoencoder(input_neuron=X.shape[1], encoding_neuron=5, learning_rate=0.093)
    autoencoder.train(X, epochs=1000)
    X_encode_data = autoencoder.encode_data(X)
    X_decode_data = autoencoder.decode_data(X_encode_data)

    print("Mean Squared Error:", np.mean((X - X_decode_data) ** 2))

    plt.plot(autoencoder.errors)
    plt.xlabel('Epochs')
    plt.ylabel('Mean Squared Error')
    plt.title('Training Error')
    plt.show()

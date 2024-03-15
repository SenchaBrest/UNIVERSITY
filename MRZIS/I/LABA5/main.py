import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report


class Perceptron:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        self.bias_output = np.zeros((1, self.output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, inputs):
        self.hidden_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = self.sigmoid(self.hidden_input)
        self.output = np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        return self.output

    def backward(self, inputs, target, output):
        error = target - output

        delta_output = error
        delta_hidden = delta_output.dot(self.weights_hidden_output.T) * self.sigmoid_derivative(self.hidden_output)

        self.weights_hidden_output += self.hidden_output.T.dot(delta_output) * self.learning_rate
        self.bias_output += np.sum(delta_output, axis=0, keepdims=True) * self.learning_rate
        self.weights_input_hidden += inputs.T.dot(delta_hidden) * self.learning_rate
        self.bias_hidden += np.sum(delta_hidden, axis=0, keepdims=True) * self.learning_rate

    def train(self, inputs, targets, epochs):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                input_data = np.array([inputs[i]])
                target_data = np.array([targets[i]])

                output = self.forward(input_data)
                self.backward(input_data, target_data, output)

    def predict(self, inputs):
        output = self.forward(inputs)
        return output

    def encode(self, inputs):
        return np.dot(inputs, self.weights_input_hidden) + self.bias_hidden


if __name__ == "__main__":
    dataset = pd.read_csv("Seed_Data.csv")
    X = dataset.iloc[:, 0:7]
    Y = dataset.iloc[:, 7]

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    size = X.shape[1]
    autoencoder = Perceptron(input_size=size, hidden_size=size // 2, output_size=size)

    inputs, targets = X, X
    autoencoder.train(inputs, targets, epochs=100)

    X_enc = autoencoder.encode(X)

    X_df = pd.DataFrame(X_enc)
    X_train, X_test, Y_train, Y_test = train_test_split(X_df, Y, test_size=0.2)

    size = X_train.shape[1]
    perceptron = Perceptron(input_size=size, hidden_size=size, output_size=1)

    inputs, targets = X_train.to_numpy(), Y_train.to_numpy()
    perceptron.train(inputs, targets, epochs=100)

    predictions = perceptron.predict(X_test.to_numpy())
    predictions = abs(np.round(predictions).astype(int)).flatten()

    accuracy = np.mean(predictions == Y_test)

    Y_test = Y_test.to_numpy()

    print(classification_report(Y_test, predictions))

    # accuracy = TP + TN / TP + TN + FP + FN
    # precision = TP / TP + FP
    # recall = TP / TP + FN


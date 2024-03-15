import numpy as np
import matplotlib.pyplot as plt


class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)
        # self.weights = np.array([1., 1])
        self.bias = np.random.rand(1)

    def activation_function(self, x):
        return 1 if x < 3 else 8

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.activation_function(weighted_sum)

    def train(self, training_inputs, labels, learning_rate, epochs):
        errors = []
        for _ in range(epochs):
            total_error = 0
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                error = label - prediction
                total_error += abs(error)

                self.weights += learning_rate * error * inputs
                self.bias += learning_rate * error
            errors.append(total_error)

        plt.plot(range(1, epochs + 1), errors)
        plt.xlabel('Epochs')
        plt.ylabel('Sum of errors')
        plt.title('Error change chart')
        plt.show()

    def plot_decision_boundary(self, training_inputs, labels):
        x_min, x_max = min(training_inputs[:, 0]) - 1, max(training_inputs[:, 0]) + 1
        y_min, y_max = min(training_inputs[:, 1]) - 1, max(training_inputs[:, 1]) + 1

        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                             np.arange(y_min, y_max, 0.01))

        z = np.array([self.predict(np.array([x, y])) for x, y in zip(xx.ravel(), yy.ravel())])
        z = z.reshape(xx.shape)

        plt.contourf(xx, yy, z, alpha=0.3, cmap=plt.cm.coolwarm)
        plt.scatter(training_inputs[:, 0], training_inputs[:, 1], c=labels, cmap=plt.cm.coolwarm)
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.title('Condition plot (decision boundary and points)')
        plt.show()


if __name__ == "__main__":
    training_inputs = np.array([[-4, -4], [-4, 2], [2, -4], [2, 2]])
    labels = np.array([1, 8, 1, 8])

    perceptron = Perceptron(input_size=2)

    learning_rate = 0.03
    epochs = 2
    perceptron.train(training_inputs, labels, learning_rate, epochs)
    perceptron.plot_decision_boundary(training_inputs, labels)

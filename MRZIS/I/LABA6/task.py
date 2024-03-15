import numpy as np

class Perceptron:
    def __init__(self, input_size, hidden_size, output_size, learning_rate="adapt"):
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
        return self.sigmoid(self.output)

    def backward(self, inputs, targets, outputs):
        if self.learning_rate == "adapt":
            error = targets - outputs

            delta_output = error * self.sigmoid_derivative(outputs)
            self.learning_rate_output = (4 * np.sum((error ** 2 * outputs * (1 - outputs)), axis=0)) / \
                            (1 + np.sum(self.hidden_output ** 2)) * \
                            (np.sum((error * outputs * (1 - outputs)) ** 2, axis=0))

            h_error = delta_output.dot(self.weights_hidden_output.T)
            self.learning_rate_hidden = (4 * np.sum((h_error ** 2 * self.hidden_output * (1 - self.hidden_output)), axis=0)) / \
                                        (1 + np.sum(self.hidden_input ** 2)) * \
                                        (np.sum((h_error * self.hidden_output * (1 - self.hidden_output)) ** 2, axis=0))

            delta_hidden = delta_output.dot(self.weights_hidden_output.T) * self.sigmoid_derivative(self.hidden_output)

            self.weights_hidden_output += self.hidden_output.T.dot(delta_output) * self.learning_rate_output
            self.bias_output += np.sum(delta_output, axis=0, keepdims=True) * self.learning_rate_output
            self.weights_input_hidden += inputs.T.dot(delta_hidden) * self.learning_rate_hidden
            self.bias_hidden += np.sum(delta_hidden, axis=0, keepdims=True) * self.learning_rate_hidden
        else:
            error = targets - outputs
            delta_output = error * self.sigmoid_derivative(outputs)
            delta_hidden = delta_output.dot(self.weights_hidden_output.T) * self.sigmoid_derivative(self.hidden_output)

            self.weights_hidden_output += self.hidden_output.T.dot(delta_output) * self.learning_rate
            self.bias_output += np.sum(delta_output, axis=0, keepdims=True) * self.learning_rate
            self.weights_input_hidden += inputs.T.dot(delta_hidden) * self.learning_rate
            self.bias_hidden += np.sum(delta_hidden, axis=0, keepdims=True) * self.learning_rate

    def train(self, inputs, targets, epochs, batch_size):
        for epoch in range(epochs):
            for i in range(0, len(inputs), batch_size):
                input_data = inputs[i:i+batch_size]
                target_data = targets[i:i+batch_size]

                output = self.forward(input_data)
                self.backward(input_data, target_data, output)

                loss = np.mean(np.square(target_data - output))
                print(f'Epoch {epoch + 1}, Batch {i // batch_size + 1}, Loss: {loss}')

    def predict(self, inputs):
        output = self.forward(inputs)
        return output


if __name__ == "__main__":
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import OneHotEncoder

    data = load_breast_cancer()
    X = data.data
    y = data.target.reshape(-1, 1)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    encoder = OneHotEncoder(sparse=False)
    y = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    input_size = X_train.shape[1]
    hidden_size = 5
    output_size = y_train.shape[1]

    perceptron = Perceptron(input_size, hidden_size, output_size)
    perceptron.train(X_train, y_train, epochs=10000, batch_size=32)

    predictions = perceptron.predict(X_test)
    accuracy = np.mean(np.round(predictions) == y_test)
    print(f'Test Accuracy: {accuracy * 100}%')

import numpy as np
import matplotlib.pyplot as plt

a, b, c, d = 0.4, 0.4, 0.08, 0.4

num_time_steps = 110
input_size = 1
hidden_size = 12
output_size = 1
lr = 0.033
start = 0
time_steps = np.linspace(start, start + 100, num_time_steps)
data = a * np.cos(b * time_steps) + c * np.sin(d * time_steps)


class RNN:
    def __init__(self, input_size, hidden_size, output_size, lr):
        self.hidden_size = hidden_size
        self.lr = lr

        std_dev = 0.01
        self.W_xh = np.random.normal(loc=0.0, scale=std_dev, size=(hidden_size, input_size))
        self.W_hh = np.random.normal(loc=0.0, scale=std_dev, size=(hidden_size, hidden_size))
        self.W_hy = np.random.normal(loc=0.0, scale=std_dev, size=(output_size, hidden_size))

        self.b_h = np.zeros((hidden_size, 1))
        self.b_y = np.zeros((output_size, 1))

        self.h_prev = np.zeros((hidden_size, 1))
        self.dh_next = np.zeros_like(self.h_prev)

    def forward(self, x):
        self.h_next = np.tanh(np.dot(self.W_xh, x) + np.dot(self.W_hh, self.h_prev) + self.b_h)
        y = np.dot(self.W_hy, self.h_next) + self.b_y
        return y

    def backward(self, x, y_true):
        dy = self.pred - y_true
        dW_hy = np.dot(dy, self.h_next.T)
        db_y = dy
        dh = np.dot(self.W_hy.T, dy) + self.dh_next
        dh_raw = (1 - self.h_next * self.h_next) * dh
        db_h = dh_raw
        dW_xh = np.dot(dh_raw, x.T)
        dW_hh = np.dot(dh_raw, self.h_prev.T)
        self.dh_next = np.dot(self.W_hh.T, dh_raw)

        self.W_xh -= self.lr * dW_xh
        self.W_hh -= self.lr * dW_hh
        self.W_hy -= self.lr * dW_hy
        self.b_h -= self.lr * db_h
        self.b_y -= self.lr * db_y

    def train(self, x_train, y_train, num_epochs):
        errors = []
        for epoch in range(num_epochs):
            total_error = 0
            self.h_prev = np.zeros((self.hidden_size, 1))
            self.dh_next = np.zeros_like(self.h_prev)
            for i in range(len(x_train)):
                x_t = x_train[i].reshape(1, 1)
                y_t = y_train[i].reshape(1, 1)

                self.pred = self.forward(x_t)
                total_error += np.sum((self.pred - y_t) ** 2)
                self.backward(x_t, y_t)

            errors.append(total_error)
            if epoch % 10 == 0:
                # self.lr *= 0.9
                print(f"Epoch {epoch}: Error = {total_error}")

        return errors


rnn = RNN(input_size, hidden_size, output_size, lr)

x_train = data[:-1].reshape(num_time_steps - 1, 1)
y_train = data[1:].reshape(num_time_steps - 1, 1)

num_epochs = 100
errors = rnn.train(x_train, y_train, num_epochs)
plt.plot(range(len(errors)), errors)
plt.xlabel('Epochs')
plt.ylabel('Total Error')
plt.title('Total Error over Training')
plt.show()

preds = []
h_prev = np.zeros((hidden_size, 1))
for i in range(num_time_steps - 1):
    x_t = x_train[i].reshape(1, 1)
    pred = rnn.forward(x_t)
    preds.append(pred.ravel()[0])

plt.scatter(time_steps[:-1], data[:-1], s=10, label='original')
plt.plot(time_steps[:-1], data[:-1])

plt.scatter(time_steps[1:], preds, label='predicted')
plt.legend()
plt.xlabel('Time Steps')
plt.ylabel('Value')
plt.title('Original vs Predicted')
plt.show()

import numpy as np
from scipy import signal


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def __call__(self, input):
        # TODO: return output
        pass

    def backward(self, output_gradient, learning_rate):
        # TODO: update parameters and return input gradient
        pass


class Conv2D(Layer):
    def __init__(self, input_shape, kernel_size, depth, transposed=False):
        super().__init__()
        self.transposed = transposed
        input_depth, input_height, input_width = input_shape
        self.depth = depth
        self.input_shape = input_shape
        self.input_depth = input_depth

        if self.transposed is False:
            self.output_shape = (depth, input_height - kernel_size + 1, input_width - kernel_size + 1)
        else:
            self.output_shape = (depth, input_height + kernel_size - 1, input_width + kernel_size - 1)

        self.kernels_shape = (depth, input_depth, kernel_size, kernel_size)
        # self.kernels = np.random.randn(*self.kernels_shape)
        # self.biases = np.random.randn(*self.output_shape)
        self.kernels = np.ones(self.kernels_shape)
        self.biases = np.ones(self.output_shape)

    def __call__(self, input):
        self.input = input
        self.output = np.copy(self.biases)

        if self.transposed is False:
            for i in range(self.depth):
                for j in range(self.input_depth):
                    self.output[i] += signal.correlate2d(self.input[j], self.kernels[i, j], "valid")
        else:
            for i in range(self.depth):
                for j in range(self.input_depth):
                    self.output[i] += signal.convolve2d(self.input[j], self.kernels[i, j], "full")

        return self.output

    def backward(self, output_gradient, learning_rate):
        kernels_gradient = np.zeros(self.kernels_shape)
        input_gradient = np.zeros(self.input_shape)

        if self.transposed is False:
            for i in range(self.depth):
                for j in range(self.input_depth):
                    kernels_gradient[i, j] = signal.correlate2d(self.input[j], output_gradient[i], "valid")
                    input_gradient[j] += signal.convolve2d(output_gradient[i], self.kernels[i, j], "full")
        else:
            for i in range(self.depth):
                for j in range(self.input_depth):
                    kernels_gradient[i, j] = signal.correlate2d(self.input[j], output_gradient[i], "valid")
                    input_gradient[j] += signal.correlate2d(output_gradient[i], self.kernels[i, j], "valid")

        self.kernels -= learning_rate * kernels_gradient
        self.biases -= learning_rate * output_gradient
        return input_gradient


class MeanSquaredErrorLoss:
    def __init__(self):
        self.predict = None
        self.target = None

    def __call__(self, target, predict):
        self.target = target
        self.predict = predict
        return np.mean((self.predict - self.target)**2) / 2

    def backward(self):
        return (self.predict - self.target) / len(self.target)


class ReLU:
    def __call__(self, x):
        x = np.array(x, dtype=np.float32)
        y = np.where(x > 0, x, 0)
        self.y = y
        return y

    def backward(self, dEdy):
        dydx = np.where(self.y <= 0, self.y, 1)
        dEdx = dEdy * dydx
        return dEdx

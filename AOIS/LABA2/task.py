import numpy as np
import matplotlib.pyplot as plt

class ADALINE:
    def __init__(self, alpha=0.01, n_in=3):
        self.alpha = alpha
        self.n_in = n_in
        self.W = np.random.rand(n_in)
        self.T = np.zeros(1)
        self.errors = []
    
    def prep_data(self, y):
        return np.array([y[i - self.n_in:i] for i in range(self.n_in, len(y))])

    def calc_error(self, x, e):
        return (1 / 2) * ((self.predict(x) - e) ** 2)
    
    def predict(self, x):
        return self.W @ x - self.T
    
    def training(self, X, E):
        for x, e in zip(X[:31 - self.n_in], E[self.n_in:31]):
            y = self.predict(x)                
            self.W += -self.alpha * (y - e) * x
            self.T += self.alpha * (y - e)

    def testing(self, X, E):
        for x, e in zip(X[31 - self.n_in:], E[31:]):
            print(f"x: {x}; y: {self.predict(x)}; e: {e}")

    def set_mean_error(self, X, E):      
        self.errors.append(np.mean([self.calc_error(x, e) for x, e in zip(X[31 - self.n_in:], E[31:])]))


def main(epochs=100, min_error=1e-5):
    model = ADALINE()

    f = lambda a, b, d, x: a * np.sin(b * x) + d
    y = f(4, 8, 0.4, np.arange(0, 4.5, 0.1))
    x = model.prep_data(y)

    for epoch in range(epochs):
        model.training(x, y)
        model.set_mean_error(x, y)
        if model.errors[-1] <= min_error:
            break
    print('Training results')
    print(f'Epochs: {epoch}; Error: {model.errors[-1]}')
    print('Testing results')
    model.testing(x, y)

    plt.plot(range(1, len(model.errors) + 1), model.errors)
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.savefig('ADALINE.png')

if __name__ == "__main__":
    main()
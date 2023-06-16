import numpy as np

class Hopfield():
    def __init__(self, Y):
        self.L = Y.shape[0]
        self.I = np.eye(Y.shape[1])
        self.W = (2 * Y - 1).T @ (2 * Y - 1) - self.L * self.I
        self.method = {
            'sync' : self._sync,
            'async' : self._async
        }
    
    def nextY(self, Y, W):
        return np.where(Y @ W <= 0, 0, 1)

    def _sync(self, Y):
        prevY = Y
        for _ in range(10):
            Y = self.nextY(Y, self.W)
            if np.allclose(Y, self.nextY(Y, self.W), atol=0):
                return Y
            if np.allclose(prevY, self.nextY(Y, self.W), atol=0):
                return
            prevY = Y

    def _async(self, Y):
        for _ in range(10):
            list_idx = list(range(Y.shape[1]))
            np.random.shuffle(list_idx)
            for idx in list_idx:
                Y[0, idx] = self.nextY(Y, self.W[:, idx])
            if np.allclose(Y, self.nextY(Y, self.W), atol=0):
                return Y
            
    def __call__(self, Y, mode='sync'):
        result = None
        if self.method.get(mode):
            result = self.method[mode](Y)
        return result

            
Y1 = [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
Y2 = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1]
Y3 = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
Y4 = [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]

model = Hopfield(np.array([Y1, Y2, Y3, Y4]))

Y_noise = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
print(model(Y=np.array([Y_noise]), mode='async'))
print(model(Y=np.array([Y_noise]), mode='sync'))
print(model(Y=np.array([Y_noise]), mode='asyc'))


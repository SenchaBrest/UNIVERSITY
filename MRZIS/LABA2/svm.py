import numpy as np


class Solver:
    def __init__(self,
                 Q: np.ndarray,
                 p: np.ndarray,
                 y: np.ndarray,
                 C: float,
                 tol: float = 1e-5) -> None:
        problem_size = p.shape[0]
        assert problem_size == y.shape[0]
        if Q is not None:
            assert problem_size == Q.shape[0]
            assert problem_size == Q.shape[1]

        self.Q = Q
        self.p = p
        self.y = y
        self.C = C
        self.tol = tol
        self.alpha = np.zeros(problem_size)

        self.neg_y_grad = -y * p

    def working_set_select(self):
        Iup = np.argwhere(
            np.logical_or(
                np.logical_and(self.alpha < self.C, self.y > 0),
                np.logical_and(self.alpha > 0, self.y < 0),
            )).flatten()
        Ilow = np.argwhere(
            np.logical_or(
                np.logical_and(self.alpha < self.C, self.y < 0),
                np.logical_and(self.alpha > 0, self.y > 0),
            )).flatten()

        find_fail = False
        try:
            i = Iup[np.argmax(self.neg_y_grad[Iup])]
            j = Ilow[np.argmin(self.neg_y_grad[Ilow])]
        except:
            find_fail = True

        if find_fail or self.neg_y_grad[i] - self.neg_y_grad[j] < self.tol:
            return -1, -1
        return i, j

    def update(self, i: int, j: int, func=None):
        Qi, Qj = self.get_Q(i, func), self.get_Q(j, func)
        yi, yj = self.y[i], self.y[j]
        alpha_i, alpha_j = self.alpha[i], self.alpha[j]

        quad_coef = Qi[i] + Qj[j] - 2 * yi * yj * Qi[j]
        if quad_coef <= 0:
            quad_coef = 1e-12

        if yi * yj == -1:
            delta = (self.neg_y_grad[i] * yi +
                     self.neg_y_grad[j] * yj) / quad_coef
            diff = alpha_i - alpha_j
            self.alpha[i] += delta
            self.alpha[j] += delta

            if diff > 0:
                if self.alpha[j] < 0:
                    self.alpha[j] = 0
                    self.alpha[i] = diff
            elif self.alpha[i] < 0:
                self.alpha[i] = 0
                self.alpha[j] = -diff

            if diff > 0:
                if self.alpha[i] > self.C:
                    self.alpha[i] = self.C
                    self.alpha[j] = self.C - diff
            elif self.alpha[j] > self.C:
                self.alpha[j] = self.C
                self.alpha[i] = self.C + diff

        else:
            delta = (self.neg_y_grad[j] * yj -
                     self.neg_y_grad[i] * yi) / quad_coef
            sum = self.alpha[i] + self.alpha[j]
            self.alpha[i] -= delta
            self.alpha[j] += delta

            if sum > self.C:
                if self.alpha[i] > self.C:
                    self.alpha[i] = self.C
                    self.alpha[j] = sum - self.C

            elif self.alpha[j] < 0:
                self.alpha[j] = 0
                self.alpha[i] = sum

            if sum > self.C:
                if self.alpha[j] > self.C:
                    self.alpha[j] = self.C
                    self.alpha[i] = sum - self.C

            elif self.alpha[i] < 0:
                self.alpha[i] = 0
                self.alpha[j] = sum

        delta_i = self.alpha[i] - alpha_i
        delta_j = self.alpha[j] - alpha_j
        self.neg_y_grad -= self.y * (delta_i * Qi + delta_j * Qj)
        return delta_i, delta_j

    def calculate_rho(self) -> float:
        sv = np.logical_and(
            self.alpha > 0,
            self.alpha < self.C,
        )
        if sv.sum() > 0:
            rho = -np.average(self.neg_y_grad[sv])
        else:
            ub_id = np.logical_or(
                np.logical_and(self.alpha == 0, self.y < 0),
                np.logical_and(self.alpha == self.C, self.y > 0),
            )
            lb_id = np.logical_or(
                np.logical_and(self.alpha == 0, self.y > 0),
                np.logical_and(self.alpha == self.C, self.y < 0),
            )
            rho = -(self.neg_y_grad[lb_id].min() +
                    self.neg_y_grad[ub_id].max()) / 2
        return rho

    def get_Q(self, i: int, func=None):
        return self.Q[i]


class OneClassSVM:
    def __init__(self,
                 nu: float = 0.1,
                 kernel: str = 'rbf',
                 degree: float = 3,
                 gamma: str = 'scale',
                 coef0: float = 0,
                 max_iter: int = 1000,
                 tol: float = 1e-5) -> None:
        self.decision_function = None
        self.n_features = None
        self.nu = nu
        self.kernel = kernel
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.max_iter = max_iter
        self.tol = tol

    def fit(self, X: np.ndarray):
        X = np.array(X)
        l, self.n_features = X.shape

        kernel_func = self.register_kernel(X.std())
        p = np.zeros(l)
        y = np.ones(l)

        def func(i):
            return kernel_func(X, X[i:i + 1]).flatten()

        # init
        alpha = np.ones(l)
        n = int(self.nu * l)
        for i in range(n):
            alpha[i] = 1
        if n < l:
            alpha[i] = self.nu * l - n
        for i in range(n + 1, l):
            alpha[i] = 0

        Q = kernel_func(X, X)
        solver = Solver(Q, p, y, 1, self.tol)
        solver.alpha = alpha
        solver.neg_y_grad = -y * np.matmul(Q, solver.alpha)

        for n_iter in range(self.max_iter):
            i, j = solver.working_set_select()
            if i < 0:
                break

            solver.update(i, j, func)
        else:
            print("OneClassSVM not coverage with {} iterations".format(
                self.max_iter))

        rho = solver.calculate_rho()
        self.decision_function = lambda x: np.matmul(
            solver.alpha,
            kernel_func(X, x),
        ) - rho
        return self

    def register_kernel(self, std: float):
        if type(self.gamma) == str:
            gamma = {
                'scale': 1 / (self.n_features * std),
                'auto': 1 / self.n_features,
            }[self.gamma]
        else:
            gamma = self.gamma

        degree = self.degree
        coef0 = self.coef0
        return {
            "linear": lambda x, y: np.matmul(x, y.T),
            "poly": lambda x, y: (gamma * np.matmul(x, y.T) + coef0) ** degree,
            "rbf": lambda x, y: np.exp(-gamma * (
                    (x ** 2).sum(1, keepdims=True) +
                    (y ** 2).sum(1) - 2 * np.matmul(x, y.T))),
            "sigmoid": lambda x, y: np.tanh(gamma * np.matmul(x, y.T) + coef0)
        }[self.kernel]

    def predict(self, X: np.ndarray):
        pred = np.sign(self.decision_function(X))
        pred[pred == 0] = -1
        return pred


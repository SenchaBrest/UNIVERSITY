import matplotlib.pyplot as plt
import numpy as np

class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None
        self.visited = set()

    def fit(self, X):
        self.labels = np.full(X.shape[0], -1)
        cluster_id = 0

        for i in range(X.shape[0]):
            if i not in self.visited:
                self.visited.add(i)
                neighbors = self.get_neighbors(X, i)

                if len(neighbors) < self.min_samples:
                    self.labels[i] = -1
                else:
                    self.expand_cluster(X, i, neighbors, cluster_id)
                    cluster_id += 1

    def expand_cluster(self, X, core_point, neighbors, cluster_id):
        self.labels[core_point] = cluster_id

        for neighbor in neighbors:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                new_neighbors = self.get_neighbors(X, neighbor)

                if len(new_neighbors) >= self.min_samples:
                    neighbors = neighbors.union(new_neighbors)

            if self.labels[neighbor] == -1:
                self.labels[neighbor] = cluster_id

    def get_neighbors(self, X, i):
        neighbors = set()
        for j in range(X.shape[0]):
            if np.linalg.norm(X[i] - X[j]) < self.eps:
                neighbors.add(j)
        return neighbors


np.random.seed(40)
cluster1 = np.random.normal(loc=0, scale=1, size=(100, 2))
cluster2 = np.random.normal(loc=10, scale=1, size=(100, 2))
cluster3 = np.random.normal(loc=30, scale=1, size=(100, 2))
uniform_points = np.random.uniform(low=-5, high=35, size=(100, 2))

# Объединение всех точек
X = np.concatenate([cluster1, cluster2, cluster3, uniform_points])
# X = np.concatenate([cluster1, cluster2, cluster3])



dbscan = DBSCAN(eps=10, min_samples=20)
dbscan.fit(X)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
for i in range(len(set(dbscan.labels))):
    cluster_points = X[dbscan.labels == i]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i % len(colors)], label=f'Cluster {i}')

plt.scatter(X[dbscan.labels == -1][:, 0], X[dbscan.labels == -1][:, 1], c='gray', marker='x', label='Noise')
plt.title('DBSCAN Clustering')
plt.legend()
plt.show()

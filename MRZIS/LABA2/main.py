import numpy as np
import matplotlib.pyplot as plt
from svm import OneClassSVM

X = 0.3 * np.random.randn(100, 2)
X_train = np.r_[X + 2, X - 2]
X = 0.3 * np.random.randn(20, 2)
X_test = np.r_[X + 2, X - 2]
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

plt.figure(figsize=(10, 5))
plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=20, edgecolors='k', label='Train Data')
plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=20, edgecolors='k', label='Test Data')
plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=20, edgecolors='k', label='Outliers')
plt.title('Data Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('One-Class SVM')
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend(loc='upper right')
plt.show()

clf = OneClassSVM(nu=0.1, kernel="rbf", gamma="scale")
clf.fit(X_train)
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
y_pred_outliers = clf.predict(X_outliers)
xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(10, 5))
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.Blues_r)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='red')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='orange')
plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=20, edgecolors='k', label='Train Data')
plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=20, edgecolors='k', label='Test Data')
plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=20, edgecolors='k', label='Outliers')
plt.title('One-Class SVM')
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend(loc='upper right')
plt.show()
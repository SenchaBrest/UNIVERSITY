import numpy as np
from scipy.stats import chi2

sequence = [20,16,14,22,31,2,18,1,26,27,28,10,8,7,11,15,17,9,0,29,13,30,5,4,3,21,23,24]

k = int(np.ceil(1 + np.log2(len(sequence))))
alpha = 0.05

n = len(sequence) / k
observed_counts, _ = np.histogram(sequence, bins=k)
expected_counts = np.full(k, n)
chi_squared_statistic = np.sum((observed_counts - expected_counts) ** 2 / expected_counts)
critical_value = chi2.ppf(1 - alpha, k - 1)

print(f"critical_value: {critical_value} \n chi_squared_statistic: {chi_squared_statistic}")
if chi_squared_statistic > critical_value:
    print("последовательность не имеет равномерного распределения.")
else:
    print("последовательность имеет равномерное распределение.")

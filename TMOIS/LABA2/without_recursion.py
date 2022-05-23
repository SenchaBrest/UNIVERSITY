import time
start_time = time.time()

def next_permutation(sequence, compare) -> bool:

	count = len(sequence)
	i = count
	# Этап № 1
	while True:
		if i < 2:
			return False # Перебор закончен
		i -= 1
		if compare(sequence[i - 1], sequence[i]):
			break
	# Этап № 2
	j = count
	while j > i and not compare(sequence[i - 1], sequence[j - 1]):
		j -= 1
	sequence[i - 1], sequence[j - 1] = sequence[j - 1], sequence[i - 1]
	# Этап № 3
	j = count
	while i < j - 1:
		j -= 1
		sequence[i], sequence[j] = sequence[j], sequence[i]
		i += 1
	return True

def less(value_0, value_1) -> bool:
	return value_0 < value_1

def greater(value_0, value_1) -> bool:
	return value_0 > value_1

count = int(input())
sequence = list(range(1, count + 1)) 

print("Lexicographic permutation:")
permutation_found = True
while permutation_found:
	print(sequence)
	permutation_found = next_permutation(sequence, less)

print("Antilexicographic permutation:")
permutation_found = True
while permutation_found:
	print(sequence)
	permutation_found = next_permutation(sequence, greater)

print("--- %s seconds ---" % (time.time() - start_time))
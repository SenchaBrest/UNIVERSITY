import numpy as np

def add_errors(binary_word, num_errors):
    error_indices = np.random.choice(len(binary_word), size=num_errors, replace=False)
    binary_word_with_errors = binary_word.copy()
    binary_word_with_errors[error_indices] = np.bitwise_xor(binary_word_with_errors[error_indices], 1)
    return binary_word_with_errors, error_indices

class IterativeCode:
    def __init__(self, length, rows, cols, n_parities):
        self.length = length
        self.rows = rows
        self.cols = cols
        self.n_parities = n_parities
        self.word = self.generate_word()
        self.matrix = self.word2matrix()
        self.parities = self.calculate_parities()

    def generate_word(self):
        return np.random.randint(2, size=self.length)

    def word2matrix(self):
        return self.word.reshape((self.rows, self.cols))

    def calculate_parities(self):
        parities = {}
        if self.n_parities >= 2:
            parities['row'] = np.sum(self.matrix, axis=1) % 2
            parities['col'] = np.sum(self.matrix, axis=0) % 2
        if self.n_parities >= 3:
            parities['diag_down'] = self.calculate_diagonal_parity_down()
        if self.n_parities >= 4:
            parities['diag_up'] = self.calculate_diagonal_parity_up()
        return parities

    def calculate_diagonal_parity_up(self):
        rows, cols = self.matrix.shape
        parities = []
        for offset in range(-(rows - 1), cols):
            diag = np.diagonal(self.matrix, offset=offset)
            parity = np.sum(diag) % 2
            parities.append(parity)
        return np.array(parities)

    def calculate_diagonal_parity_down(self):
        flipped_matrix = np.fliplr(self.matrix)
        rows, cols = flipped_matrix.shape
        parities = []
        for offset in range(-(rows - 1), cols):
            diag = np.diagonal(flipped_matrix, offset=offset)
            parity = np.sum(diag) % 2
            parities.append(parity)
        return np.array(parities)[::-1]

    def get_indices(self, str, index):
        match str:
            case 'row':
                return self.get_row_indices(index)
            case 'col':
                return self.get_col_indices(index)
            case 'diag_down':
                return self.get_diagonal_indices_down(index)
            case 'diag_up':
                return self.get_diagonal_indices_up(index)

    def get_row_indices(self, row_index):
        return [(row_index, col_idx) for col_idx in range(self.matrix.shape[1])]

    def get_col_indices(self, col_index):
        return [(row_idx, col_index) for row_idx in range(self.matrix.shape[0])]

    def get_diagonal_indices_up(self, parity_index):
        rows, cols = self.matrix.shape
        offset = parity_index - (rows - 1)
        diag = np.diagonal(self.matrix, offset=offset)
        if offset >= 0:
            return [(i, i + offset) for i in range(len(diag))]
        else:
            return [(i - offset, i) for i in range(len(diag))]

    def get_diagonal_indices_down(self, parity_index):
        indices = self.get_diagonal_indices_up(parity_index)
        return [(self.rows - 1 - index[0], index[1]) for index in indices]

    def __str__(self):
        return f"Слово: {self.word}\n" + \
            f"Матрица:\n {self.matrix}\n" + \
            f"Паритеты строк: {self.parities['row']}\n" + \
            f"Паритеты столбцов: {self.parities.get('col')}\n" + \
            f"Паритеты диагонали (вниз): {self.parities.get('diag_down')}\n" + \
            f"Паритеты диагонали (вверх): {self.parities.get('diag_up')}\n"


class IterativeCodeSend(IterativeCode):
    def combine_parities_and_word(self):
        parities_array = [self.word]
        for key in list(self.parities.keys()):
            parities_array.append(self.parities[key])
        return np.concatenate(parities_array)


class IterativeCodeReceive(IterativeCode):
    def __init__(self, length, rows, cols, n_parities, word):
        super().__init__(length, rows, cols, n_parities)
        self.unpack(word)
        self.matrix = self.word2matrix()
        self.parities = self.calculate_parities()
        self.errors = self.find_errors()

    def unpack(self, word):
        splits = [
            self.length, 
            self.length + self.rows, 
            self.length + self.rows + self.cols,
            self.length + 2 * (self.rows + self.cols) -1]
        self.word = word[:splits[0]]

        self.current_parities = {}
        if self.n_parities >= 2:
            self.current_parities['row'] = word[splits[0]:splits[1]]
            self.current_parities['col'] = word[splits[1]:splits[2]]
        if self.n_parities >= 3:
            self.current_parities['diag_down'] = word[splits[2]:splits[3]]
        if self.n_parities >= 4:
            self.current_parities['diag_up'] = word[splits[3]:]

    def calculate_parity(self, key):
        return self.parities.get(key)

    def find_errors(self):
        errors = {}
        for key in list(self.parities.keys()):
            errors_in_parities = (np.where(self.current_parities[key] != self.parities[key])[0]).tolist()
            for error_index in errors_in_parities:
                errors[key] = set()
                for position in self.get_indices(key, error_index):
                    errors[key].add(position)
        if len(errors.keys()) < self.n_parities: return set()
        return set.intersection(*errors.values())

    def fix_errors(self):
        if self.errors == set(): return self.word
        matrix = self.matrix.copy()
        for x, y in self.errors:
            print(~matrix[x][y])
            matrix[x][y] ^= 1
        return matrix.flatten()

    def __str__(self):
        return super().__str__() + \
            f"Найденные ошибки: {self.errors}\n" + \
            f"Исправленное слово: {self.fix_errors()}"


if __name__=="__main__":
    length = 12
    rows, cols = 3, 4
    num_parities = 2
    num_errors = 3

    code2send = IterativeCodeSend(length, rows, cols, num_parities)
    print(code2send)

    word2send = code2send.combine_parities_and_word()
    print("Слово с паритетами:", word2send)
    word2send, _ = add_errors(word2send, num_errors)
    print("Слово с ошибками:", word2send)

    code2receive = IterativeCodeReceive(length, rows, cols, num_parities, word2send)
    print(code2receive)
import numpy as np
from code2d import IterativeCode, IterativeCodeReceive, IterativeCodeSend, add_errors

class IterativeCode3D:
    def __init__(self, length, x, y, z, n_parities):
        self.length = length
        self.x, self.y, self.z = x, y, z
        self.n_parities = n_parities
        self.slicis = [
            IterativeCodeSend(
                length // z, x, y, n_parities if n_parities < 5 else n_parities - 1
            ) for _ in range(z)
        ]
        self.word = np.concatenate([slice.word for slice in self.slicis])
        self.matricis = [slice.matrix for slice in self.slicis]
        self.parities = self.combine_parities([slice.parities for slice in self.slicis])
        if n_parities == 5:
            self.parities['z'] = self.calculate_z_parity()

    def combine_parities(self, parities):
        combined_parities = {key: [] for key in parities[0].keys()}
        for d in parities:
            for key in d:
                combined_parities[key].append(d[key])
        for key in combined_parities:
            combined_parities[key] = np.array(combined_parities[key])
        return combined_parities

    def calculate_z_parity(self):
        z_parity = np.zeros((self.x, self.y), dtype=int)
        for matrix in self.matricis:
            z_parity += matrix
        z_parity %= 2
        return z_parity

    def get_indices(self, str, index, z):
        match str:
            case 'row':
                return self.get_row_indices(index, z)
            case 'col':
                return self.get_col_indices(index, z)
            case 'diag_down':
                return self.get_diagonal_indices_down(index, z)
            case 'diag_up':
                return self.get_diagonal_indices_up(index, z)
            case 'z':
                return self.get_z_parity_indices(x=index, y=z)

    def get_row_indices(self, row_index, z):
        return [(row_index, col_idx, z) for col_idx in range(self.matricis[z].shape[1])]

    def get_col_indices(self, col_index, z):
        return [(row_idx, col_index, z) for row_idx in range(self.matricis[z].shape[0])]

    def get_diagonal_indices_up(self, parity_index, z):
        rows, cols = self.matricis[z].shape
        offset = parity_index - (rows - 1)
        diag = np.diagonal(self.matricis[z], offset=offset)
        if offset >= 0:
            return [(i, i + offset, z) for i in range(len(diag))]
        else:
            return [(i - offset, i, z) for i in range(len(diag))]

    def get_diagonal_indices_down(self, parity_index, z):
        indices = self.get_diagonal_indices_up(parity_index, z)
        return [(self.x - 1 - index[0], index[1], z) for index in indices]

    def get_z_parity_indices(self, x, y):
        return [(x, y, z) for z in range(self.z)]

class IterativeCode3DSend(IterativeCode3D):
    def combine_parities_and_word(self):
        array = []
        for slice in self.slicis:
            array.append(slice.combine_parities_and_word())
        if self.n_parities == 5:
            array.append(self.parities['z'].flatten())
        return np.concatenate(array)

class IterativeCode3DReceive(IterativeCode3D):
    def __init__(self, length, x, y, z, n_parities, word):
        super().__init__(length, x, y, z, n_parities)
        self.unpack(word)

        self.errors = self.find_errors()
        print(self.errors)
        print(self.fix_errors())
    
    def unpack(self, word):
        if self.n_parities == 5:
            z_parities = word[-(self.x * self.y):].reshape(self.x, self.y)
            word = word[:-(self.x * self.y)]
        split_word = np.array_split(word, self.z)
        split_word = [arr.tolist() for arr in split_word]

        slicis = [
            IterativeCodeReceive(
                self.length // self.z,
                self.x, 
                self.y, 
                self.n_parities if self.n_parities < 5 else self.n_parities - 1, 
                np.array(split_word[i])
            ) for i in range(self.z)
        ]

        self.word = np.concatenate([slice.word for slice in slicis])
        self.matricis = [slice.matrix for slice in slicis]
        self.current_parities = self.combine_parities([slice.current_parities for slice in slicis])
        self.parities = self.combine_parities([slice.parities for slice in slicis])
        if self.n_parities == 5:
            self.current_parities['z'] = z_parities
            self.parities['z'] = self.calculate_z_parity()
    
    def find_errors(self):
        errors = {}
        for key in list(self.parities.keys()):
            errors[key] = set()
            for i in range(self.z):
                errors_in_parities = (np.where(self.current_parities[key][i] != self.parities[key][i])[0]).tolist()
                for error_index in errors_in_parities:
                    for position in self.get_indices(key, error_index, i):
                        errors[key].add(position)
        print(errors)
        if len(errors.keys()) < self.n_parities: return set()
        return set.intersection(*errors.values())

    def fix_errors(self):
        if self.errors == set(): return self.word
        matricis = self.matricis.copy()
        for x, y, z in self.errors:
            matricis[z][x][y] ^= 1
        return np.array(matricis).flatten()


        
        


code2send = IterativeCode3DSend(24, 6, 2, 2, 5)
word2send = code2send.combine_parities_and_word()
print(word2send)
word2send, _ = add_errors(word2send, 5)
print(word2send)
print()
print(code2send.word)

code2receive = IterativeCode3DReceive(24, 6, 2, 2, 5, word2send)



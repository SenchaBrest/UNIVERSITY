import pickle as p

def export_to_pickle(obj, path):
    with open(path, 'wb') as f:
        p.dump(obj, f)

def export_from_pickle(path):
    with open(path, 'rb') as f:
        return p.load(f)


def export_to_file(self, name, path, orient=False):

    matrix = list(self.graph.adjacency_matrix())

    with open(path, 'w') as f:
        if orient:
            f.write(f'{name}:ORIENT; ')
        else:
            f.write(f'{name}:UNORIENT; ')

        for i in range(len(matrix)):
            if i == len(matrix) - 1:
                f.write(str(i)+ '; ')
            else:
                f.write(str(i) + ',')

        for i, _ in enumerate(matrix):
            for j, _ in enumerate(matrix):
                if matrix[i][j] == 1:
                    if i == len(matrix) - 1 and j == len(matrix) - 1:
                        f.write(f'{i}->{j}; ')
                    else:
                        f.write(str(i) + '->' + str(j) + ',')

def export_from_file(path):

    with open(path, 'r') as f:
        data = f.read()

        data = data.split('; ')
        data[0] = data[0].split(':')
        data[1] = data[1].split(',')
        data[2] = data[2].split(',')

        name = data[0][0]
        orient = data[0][1]
        nodes = data[1]
        edges = data[2]
        matrix = [[0 for i in range(len(nodes))] for j in range(len(nodes))]

        for edge in edges:
            if edge != '':
                edge = edge.split('->')
                matrix[int(edge[0])][int(edge[1])] = 1
        return matrix, name, orient


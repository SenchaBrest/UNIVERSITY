import csv
from task1 import rn_str

class HashTable:
    def __init__(self, size, key_field, fields):
        self.size = size
        self.key_field = key_field
        self.fields = fields
        self.table = [None] * size
        self.collision_count = 0
        self.search_count = 0
        self.n_records = 0
        
    def hash_function(self, key, h=None):
        if h is None:    
            h = 1
            for char in key:
                h *= ord(char)
        h = str(h ** 2)
        middle = len(h) // 2
        h = int(h[middle - 1:middle + 2]) % self.size

        i = 0
        while i < self.size:
            if self.table[h] is None or self.table[h][0] == key:
                break
            else:
                self.collision_count += 1
                i += 1
                h = (h + i) % self.size
        return h
    
    def add_record(self, values):
        if self.n_records == self.size:
            print("Table is full! I can not add this record!")
            return
        self.n_records += 1
        key_value = values[0]
        h = self.hash_function(key_value)
        self.table[h] = values

        self.table[h].append([self.n_records, self.collision_count])    
    
    def remove_record(self, key_value):
        h = self.hash_function(key_value)
        self.table[h] = None
        self.n_records -= 1
    
    def update_record(self, key_value, new_values):
        h = self.hash_function(key_value)
        self.table[h] = new_values
    
    def search_record(self, key_value):
        h = self.hash_function(key_value)
        return self.table[h]
    
    def write_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.key_field] + self.fields)
            for record in self.table:
                if record is not None:
                    writer.writerow(record)
                    
    def from_csv(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.key_field, *self.fields = next(reader)
            self.table = [None] * self.size
            for row in reader:
                self.add_record(row)

    def create_records(self, n, numerical=True):
        for i in range(n):
            self.add_record([str(i + 1) if numerical else rn_str(),
                 *[rn_str() for _ in range(len(self.fields))]])

    def collision_probability(self):
        n = 0
        for i in range(len(self.table)):
            if self.table[i] is None:
                continue
            else:
                n += 1
        return self.collision_count / n

    def average_search_count(self):
        total_search_count = 0
        for record in self.table:
            if record is not None:
                key_value = record[0]
                self.search_record(key_value)
                total_search_count += self.search_count
                self.search_count = 0
        return total_search_count / len(self.table)
    
if __name__ == '__main__':
    N = 64
    hash_table = HashTable(N, 'key', ['first', 'second', 'third'])

    hash_table.from_csv('table.csv')
    hash_table.write_to_csv('hash_table.csv')

    print(f"collision_probability: {hash_table.collision_probability()}")
    print(f"average_search_count: {hash_table.average_search_count()}")
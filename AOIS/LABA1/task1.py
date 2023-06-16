import random as rn
import string
import csv

def rn_str():
    return ''.join(rn.choices(string.ascii_letters, k=rn.randint(5, 11)))

class Table:
    def __init__(self, key_field, fields):
        self.key_field = key_field
        self.fields = fields
        self.table = []
        
    def add_record(self, values):
        self.table.append(values)

    def remove_record(self, key_value):
        for i in range(len(self.table)):
            if self.table[i][0] == key_value:
                self.table.pop(i)
                break

    def update_record(self, key_value, new_values):
        for i in range(len(self.table)):
            if self.table[i][0] == key_value:
                self.table[i] = new_values
                break

    def search_record(self, key_value):
        for record in self.table:
            if record[0] == key_value:
                return record
        return None
    
    def write_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.key_field] + self.fields)
            for record in self.table:
                writer.writerow(record)

    def from_csv(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.key_field, *self.fields = next(reader)
            self.table = []
            for row in reader:
                self.table.append(row)

    def create_records(self, n, numerical=True):
        for i in range(n):
            self.add_record([str(i + 1) if numerical else rn_str(),
                 *[rn_str() for _ in range(len(self.fields))]])

if __name__ == '__main__':
    n = 40
    table = Table('key', ['first', 'second', 'third'])
    table.create_records(n, False)
    table.write_to_csv('table.csv')


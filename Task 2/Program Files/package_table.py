import csv


class Package:
    def __init__(self, data):
        self.address = '{0} ({1})'.format(data[0], data[3])
        self.city = data[1]
        self.state = data[2]
        self.zip = data[3]
        self.deadline = None if data[4] == 'EOD' else data[4]
        self.weight = data[5]
        self.note = data[6]
        self.status = 'at hub'

    def __str__(self):
        return (f'Delivery address: {self.address[:-7]}\n'
                f'City: {self.city}\n'
                f'Zip code: {self.zip}\n'
                f'Deadline: {self.deadline}\n' 
                f'Weight: {self.weight}\n'
                f'Status: {self.status}')


class PackageTable:
    def __init__(self, size=10, file='packages.csv'):
        self.size = size
        self.store = [None] * size
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                self.insert(int(line[0]), Package(line[1:]))

    def __str__(self):
        table_str = ""
        for i in range(self.size):
            chain_list = self.store[i]
            if chain_list:
                table_str += f"Slot {i}:\n"
                for key, value in chain_list:
                    table_str += f"\t{key}: {value}\n"
        return table_str

    def __hash(self, key):
        num_key = int(key)
        return num_key % self.size

    def insert(self, key, value):
        index = self.__hash(key)
        if self.store[index] is None:
            self.store[index] = []
        self.store[index] += [(key, value)]

    def lookup(self, key):
        index = self.__hash(key)
        chain_list = self.store[index]
        for k, value in chain_list:
            if k == key:
                return value
        return None

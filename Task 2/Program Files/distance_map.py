import csv


class DistanceMap:
    def __init__(self, map_file="map.csv"):
        self.addresses = dict()
        self.distances = []
        with open(map_file, 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                self.addresses[line[0]] = i
                self.distances.append([float(d) for d in line[1:]])

    # Get distances from two points
    def distance(self, address1, address2):
        index1 = self.addresses.get(address1)
        index2 = self.addresses.get(address2)
        return self.distances[index1][index2]

    # Get the closest address from the available addresses
    def closest(self, address, available_addresses):
        min_distance = float('inf')
        min_address = None
        for a in available_addresses:
            distance = self.distance(address, a)
            if distance < min_distance:
                min_distance = distance
                min_address = a
        return min_distance, min_address

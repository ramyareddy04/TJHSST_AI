import csv
import math
import random

k = 6

actual = ['Brown Dwarf', 'Red Dwarf', 'White Dwarf', 'Main Sequence', 'Supergiant', 'Hypergiant']

class Star():

    def __init__(self, vector):
        for i in range(4): vector[i] = float(vector[i])
        self.temp, self.luminosity, self.radius, self.avm, self.type = vector
        if self.type != -1:
            self.temp = math.log(self.temp)
            self.luminosity = math.log(self.luminosity)
            self.radius = math.log(self.radius)
    
    def getType(self):
        return self.type

    def getTemp(self):
        return self.temp

    def getLuminosity(self):
        return self.luminosity

    def getRadius(self):
        return self.radius

    def getAVM(self):
        return self.avm

    def data(self):
        return (self.temp, self.luminosity, self.radius, self.avm, self.type)

    def mse(self, other):
        return pow(self.getTemp()-other.getTemp(), 2) + pow(self.getLuminosity()-other.getLuminosity(), 2) + pow(self.getRadius()-other.getRadius(), 2) + pow(self.getAVM()-other.getAVM(), 2)

def assign(kmeans, clusters, data):
    for star in data:
        MSE = [star.mse(mean) for mean in kmeans]
        idx = MSE.index(min(MSE))
        clusters[idx].append(star)

def new_mean(cluster):
    avgTemp = sum([star.getTemp() for star in cluster])/len(cluster)
    avgLuminosity = sum([star.getLuminosity() for star in cluster])/len(cluster)
    avgRadius = sum([star.getRadius() for star in cluster])/len(cluster)
    avgAVM = sum([star.getAVM() for star in cluster])/len(cluster)
    return Star([avgTemp, avgLuminosity, avgRadius, avgAVM, -1])

dataset = []

with open('star_data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i!= 0:
            dataset.append(Star(row[:-2]))

means = random.sample(dataset, k)
groups = [[] for i in range(k)]

assign(means, groups, dataset)
sizes = [len(groups[i]) for i in range(k)]
dStars = len(dataset)

while dStars != 0:
    means = [new_mean(cluster) for cluster in groups]
    groups = [[] for i in range(k)]

    assign(means, groups, dataset)
    newSizes = [len(groups[i]) for i in range(k)]
    dStars = sum([abs(newSizes[i]-sizes[i]) for i in range(k)])
    sizes = newSizes

for i in range(k):
    print('Mean: ', means[i].data())
    for star in groups[i]:
        print(actual[int(star.getType())], star.data())
    print()
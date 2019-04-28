import numpy as np
from math import sqrt


class KNN:
    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.classes = self.classes()
        self.distance = self.euclid

    def classes(self):
    classes = []
    d = self.data
    for i in d:
        if not(i['y'] in classes):
            classes.append(i['y'])
    return classes

    def setDistance(self, method):
        if method == 'euclidean':
            self.distance == self.euclid
        elif method == 'manhattan':
            self.distance == self.manhat
        else:
            print('no such method')

    def euclid(self, a, b):
        if(len(a) == len(b)):
            total = 0
            for i in range(0, len(a)):
                delta = a[i] - b[i]
                squaredDelta = delta**2
                total += squaredDelta
            distance = sqrt(total)
            return distance
        else:
            print('Vectors must be of same size')

    def manhat(self, a, b):
        if(len(a) == len(b)):
            total = 0
            for i in range(0, len(a)):
                delta = abs(a[i] - b[i])
                total += squaredDelta
            return total
        else:
            print('Vectors must be of same size')

    def predict(self, vec):
        distance = []
        for i in self.data:
            dist = self.distance(i['X'], vec)
            distance.append({'y': i['y'], 'dist': dist})
        sortedDistance = sorted(distance, key=lambda i: i['dist'])

        pos = 0
        neg = 0
        count = 0
        while pos < self.k or neg < self.k:
            if sortedDistance[count]['y'] == -1:
                neg += 1
            else:
                pos += 1
            count += 1

        if pos > neg:
            return 1
        else:
            return -1

        # classesCount = [0] * len(self.classes)
        # counter = 0
        # while not(self.k in classesCount):
        #     ind = self.classes.index(self.data[counter]['y'])
        #     classesCount[ind] += 1
        #     counter += 1
        # finalInd = classesCount.index(self.k)
        # return self.classes[finalInd]

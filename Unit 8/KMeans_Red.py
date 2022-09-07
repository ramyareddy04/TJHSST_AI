import math
import random
import urllib.request
import io
import sys
from PIL import Image
import statistics
from statistics import mode
import time

matrix = [[0,0,2],[1,1,0]]

def mse(mean, pix):
    return pow(mean[0]-pix[0],2)+pow(mean[1]-pix[1],2)+pow(mean[2]-pix[2],2)

def get_dataset(img):
    coords = []
    colors = []
    width, height = img.size
    pix = img.load()
    for i in range(width):
        for j in range(height):
            coords.append([i,j])
            colors.append(pix[i,j])
    return coords, colors

def naive(img, k):
    
    def classify(val):
        if k == 8:
            return 0 if val < 128 else 255
        else:
            if val < 255//3: return 0
            elif val > 255*2//3: return 255
            return 127

    width, height = img.size
    fin = Image.new("RGB", size=(width, height+(width//k)))
    org = img.load()
    pix = fin.load()

    colors = set()
    for i in range(width):
        for j in range(height):
            RGB = org[i, j]
            color = (classify(RGB[0]), classify(RGB[1]), classify(RGB[2]))
            colors.add(color)
            dR = org[i, j][0] - color[0]
            dG = org[i, j][1] - color[1]
            dB = org[i, j][2] - color[2]
            for r in range(len(matrix)):
                for c in range(len(matrix[0])):
                    if i+r < width and j+c <height:
                        temp = org[i+r, j+c]
                        if temp != 0:
                            ratio = matrix[r][c]/4
                            org[i+r, j+c] = (int(temp[0]+ratio*dR), int(temp[1]+ratio*dG), int(temp[2]+ratio*dB))
            pix[i, j] = color

    colors = list(colors)
    for i in range(width):
        color = int(i//(width/len(colors)))
        for j in range(height, fin.size[1]):
            pix[i, j] = colors[color]

    fin.save("naive.png")
    fin.show()

def kmeans_alg(img, k, d1, d2):

    pix = img.load()

    pixels = d1     # coords
    dataset = d2    # colors
    unique = list(set(dataset))

    def cluster_means():
        temp = unique.copy()
        means = set()
        means.add(mode(dataset))
        temp.remove(mode(dataset))
        while len(means) != k:
            if len(means) == k-1: times = 1
            else: times = random.choice([1,2])
            MSE = [min([mse(mean, m) for m in means]) for mean in temp]
            newC = random.choices(MSE, weights=MSE, k=times)
            for val in newC:
                temp2 = temp[MSE.index(val)]
                means.add(temp2)
                temp.remove(temp2)
        return list(means)

    def assign(kmeans, clusters, coords, data):
        uniqueDif = {}
        for color in unique:
            MSE = [mse(mean, color) for mean in kmeans]
            uniqueDif[color] = MSE.index(min(MSE))
        for i, color in enumerate(data):
            idx = uniqueDif[color]
            clusters[idx].append(coords[i])

    def sierra_lite(src, out, width, height, colors):
        for i in range(width):
            for j in range(height):
                MSE = [mse(mean, src[i, j]) for mean in colors]
                color = colors[MSE.index(min(MSE))]
                dR = src[i, j][0] - color[0]
                dG = src[i, j][1] - color[1]
                dB = src[i, j][2] - color[2]
                for r in range(len(matrix)):
                    for c in range(len(matrix[0])):
                        if i+r < width and j+c <height:
                            temp = src[i+r, j+c]
                            if temp != 0:
                                ratio = matrix[r][c]/4
                                src[i+r, j+c] = (int(temp[0]+ratio*dR), int(temp[1]+ratio*dG), int(temp[2]+ratio*dB))
                out[i, j] = color

    def change_color_with_dithering(src, kmeans, clusters):
        fin = src.load()
        sierra_lite(pix, fin, img.size[0], img.size[1], kmeans)
        for i in range(img.size[0]):
            color = int(i//(img.size[0]/k))
            for j in range(img.size[1], src.size[1]):
                fin[i, j] = kmeans[color] 
        src.save("kmeansout.png")

    def change_color(src, kmeans, clusters):
        fin = src.load()
        for i, idx in enumerate(clusters):
            for coord in idx:
                fin[coord[0], coord[1]] = kmeans[i] 
        for i in range(img.size[0]):
            color = int(i//(img.size[0]/k))
            for j in range(img.size[1], src.size[1]):
                fin[i, j] = kmeans[color] 
        src.save("kmeansout.png")

    def new_mean(cluster):
        avgR = 0
        avgG = 0
        avgB = 0
        for val in cluster:
            avgR += pix[val[0], val[1]][0]
            avgG += pix[val[0], val[1]][1]
            avgB += pix[val[0], val[1]][2]
        return (avgR/len(cluster), avgG/len(cluster), avgB/len(cluster))

    # means = random.sample(unique, k)
    means = cluster_means()
    groups = [[] for i in range(k)]

    assign(means, groups, pixels, dataset)
    sizes = [len(groups[i]) for i in range(k)]
    dColors = len(dataset)

    while dColors != 0:
        means = [new_mean(cluster) for cluster in groups]
        groups = [[] for i in range(k)]

        assign( means, groups, pixels, dataset)
        newSizes = [len(groups[i]) for i in range(k)]
        dColors = sum([abs(newSizes[i]-sizes[i]) for i in range(k)])
        sizes = newSizes
    
    for color in range(k):
        means[color] = (int(means[color][0]), int(means[color][1]), int(means[color][2]))
        
    fin = Image.new("RGB", size=(img.size[0], img.size[1]+(img.size[0])//k), color=0)
    change_color_with_dithering(fin, means, groups)

URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read())
coord_dataset, color_dataset = get_dataset(Image.open(f))
src = Image.open(f)
kmeans_alg(src, int(sys.argv[2]), coord_dataset, color_dataset)
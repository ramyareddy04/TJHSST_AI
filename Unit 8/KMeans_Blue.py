import math
import random
import urllib.request
import io
import sys
from PIL import Image

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
            pix[i, j] = (classify(RGB[0]), classify(RGB[1]), classify(RGB[2]))
            colors.add(pix[i, j])
    colors = list(colors)
    for i in range(width):
        color = int(i//(width/len(colors)))
        for j in range(height, fin.size[1]):
            pix[i, j] = colors[color]
            
    fin.save("naiveout.png")

def kmeans_alg(img, k, d1, d2):

    pix = img.load()

    pixels = d1     # coords
    dataset = d2    # colors
    unique = list(set(dataset))

    def assign(kmeans, clusters, coords, data):
        uniqueDif = {}
        for color in unique:
            MSE = [mse(mean, color) for mean in kmeans]
            uniqueDif[color] = MSE.index(min(MSE))
        for i, color in enumerate(data):
            idx = uniqueDif[color]
            clusters[idx].append(coords[i])

    def change_color(src, kmeans, clusters, coords):
        fin = src.load()
        for i, idx in enumerate(clusters):
            for coord in idx:
                fin[coord[0], coord[1]] = (int(kmeans[i][0]), int(kmeans[i][1]), int(kmeans[i][2]))
        for i in range(img.size[0]):
            color = int(i//(img.size[0]/k))
            for j in range(img.size[1], src.size[1]):
                fin[i, j] = (int(kmeans[color][0]), int(kmeans[color][1]), int(kmeans[color][2]))
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

    means = random.sample(unique, k)
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
    
    fin = Image.new("RGB", size=(img.size[0], img.size[1]+(img.size[0])//k), color=0)
    change_color(fin, means, groups, pixels)

URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read())
coord_dataset, color_dataset = get_dataset(Image.open(f))
src = Image.open(f)
kmeans_alg(src, int(sys.argv[2]), coord_dataset, color_dataset)
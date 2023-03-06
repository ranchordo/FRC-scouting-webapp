import requests
import json
import urllib
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import colorsys

key = None
cx = None

def getCreds():
    global key, cx
    if key is not None and cx is not None:
        return key, cx
    with open("cse_creds.json", 'r') as f:
        js = json.loads(f.read())
        key = js['key']
        cx = js['cx']
    return key, cx

def getUrls(query, n):
    key, cx = getCreds()
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={ key }&cx={ cx }&num={ n }&searchType=image&q={ query }"
    js = json.loads(requests.get(url).text)
    urls = [i['image']['thumbnailLink'] for i in js['items']]
    return urls


def downloadImage(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def getImageFlatnessScore(img):
    flattened = np.reshape(img, ((img.shape[0] * img.shape[1]), 3))
    scalared = np.multiply(flattened, [100000, 100, 1])
    sums = scalared.sum(axis=1)
    _, counts = np.unique(sums, return_counts=True)
    pixels = sum(sorted(counts, reverse=True)[:128])
    return pixels / (1.0 * img.shape[0] * img.shape[1])

def getBestImage(imgs):
    flatnesses = [getImageFlatnessScore(img) for img in imgs]
    idxmax = np.argmax(flatnesses)
    return imgs[idxmax]

def getBestColor(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (120, 120))
    img = img.reshape(img.shape[0] * img.shape[1], 3)
    clf = KMeans(n_clusters=6, n_init='auto')
    labels = clf.fit_predict(img)
    counts = Counter(labels)
    colors = clf.cluster_centers_
    sorted_idxs = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    idxs = [i[0] for i in sorted_idxs]
    for idx in idxs:
        hsv = colorsys.rgb_to_hsv(*(colors[idx] / 255.0))
        if hsv[1] > 0.15 and hsv[2] > 0.20:
            return colors[idx]
    return colors[idxs[0]]

def getTeamColor(team):
    # return (1,1,1)
    urls = getUrls(f"frc {team} logo", 4)
    imgs = [downloadImage(url) for url in urls]
    img = getBestImage(imgs)
    return (getBestColor(img) / 255.0)
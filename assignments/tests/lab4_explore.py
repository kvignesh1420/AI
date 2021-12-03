
from pprint import pprint
import math
import numpy as np

def euclidean_distance(node1, node2):
  """Calculate the euclidean distance between two nodes

  Args:
    node1: start node of type `Node`.
    node2: destination node of type `Node`.

  Returns: euclidean distance between the two nodes
  """
  return round(math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2), 2)


points = (
    (1, 6),
    (1002, 20),
    (498, 651),
    (6, 10),
    (510,622),
    (503, 632),
    (4, 9),
    (1010, 25),
    (1006, 30),
    (502, 680)
)

res = [[0 for _ in range(len(points))] for _ in range(len(points))]
for i in range(len(points)):
    for j in range(len(points)):
        res[i][j] = euclidean_distance(points[i], points[j])
res = np.matrix(res)
pprint(res)

np.savetxt("foo_t.csv", res, delimiter=",", fmt='%.2f')

import pandas as pd

df = pd.read_csv('foo_t.csv', header=0)
print(df)
df.columns = ["A","B","C","D","E","F","G","H","I","J"]
print(df.columns)
df = df.set_index(df.columns)
print(df)
df.to_html("foo_t.html")

def single_linkage_distance(c1, c2):
    dist = math.inf
    pair = ("","")
    for e1 in c1:
        for e2 in c2:
            dist_t = df[e1][e2]
            if dist_t < dist:
                dist = dist_t
                pair = (e1,e2)
    return (dist, pair)


def complete_linkage_distance(c1, c2):
    dist = -math.inf
    pair = ("","")
    for e1 in c1:
        for e2 in c2:
            dist_t = df[e1][e2]
            if dist_t > dist:
                dist = dist_t
                pair = (e1,e2)
    return (dist, pair)

clusters = [["A"],["B"],["C"],["D"],["E"],["F"],["G"],["H"],["I"],["J"]]
while len(clusters) > 3:
    print("ITER: START")
    min_dist = math.inf
    min_pair = ("","")
    for i in range(len(clusters)-1):    
        # distances = []
        for j in range(i+1, len(clusters)):
            cluster_1 = clusters[i]
            cluster_2 = clusters[j]
            # dist_t = single_linkage_distance(cluster_1, cluster_2)
            dist_t = complete_linkage_distance(cluster_1, cluster_2)
            # distances.append(dist_t)
            # dist_t = min(distances)
            # print(dist_t)
            if dist_t[0] < min_dist:
                min_dist = dist_t[0]
                min_pair = (cluster_1, cluster_2)

    print(min_dist, min_pair)
    merged_cluster = min_pair[0] + min_pair[1]
    print(min_dist, merged_cluster)
    clusters.remove(min_pair[0])
    clusters.remove(min_pair[1])
    clusters.append(merged_cluster)
    print(clusters)


# K-MEANS

k = 3
old_centroids = [[1, 6], [1002, 20], [498, 651]]
new_centroids = [[], [], []]
iter = 0
while list(new_centroids) != list(old_centroids):
    print(f"ITER: {iter}")
    if new_centroids[0] != []:
        centroids = new_centroids
        old_centroids = new_centroids
    else:
        centroids = old_centroids
    mapping = [-1 for _ in range(len(points))]
    distances = []
    c_points = [[],[],[]]
    for i in range(len(points)):
        min_dist = math.inf
        dists = []
        for idx, c in enumerate(centroids):
            dist_t = euclidean_distance(c, points[i])
            dists.append(dist_t)
            if  dist_t < min_dist:
                min_dist = dist_t
                mapping[i] = idx
        # print(mapping[i], min_dist)
        distances.append(dists)
        c_points[mapping[i]].append(points[i])

    print(mapping)
    print(np.round(np.matrix(distances), 3))
    res = np.round(np.matrix(distances), 3)
    np.savetxt(f"kmeans_b_{iter}.csv", res, delimiter=",", fmt='%.3f')
    print(c_points)

    sorted(list(zip(mapping, points)))
    for i in range(k):
        res = np.round(np.mean(np.matrix(c_points[i]), axis=0), 3)[0]
        new_centroids[i] = [res[0], res[1]]

    print(old_centroids)
    print(new_centroids)
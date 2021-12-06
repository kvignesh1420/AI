#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
This module maintains the implementations of the
KNN and KMeans algorithms.
"""
from abc import ABC, abstractmethod
from collections import defaultdict

import numpy as np
import pandas as pd


class Classifier(ABC):
  """An abstract base class for defining classifiers"""

  @abstractmethod
  def train(self):
    """train method which has to be implemented
    by the sub-classes of Classifier."""
    pass

  @abstractmethod
  def test(self):
    """test method which has to be implemented
    by the sub-classes of Classifier."""
    pass

class KNearestNeighbors(Classifier):
  def __init__(self, k, dist_function, unitw, train_file, test_file):
    """The K Nearest Neighbors classifier

    Args:
      k: Number of nearest neighbors to consider for classification.
      dist_function: distance function to calculate closeness of neighbors.
      unitw: whether to use unit voting weights w.r.t neighbors,
        if not set we use 1/d as the weight of a neibhbor.
      train_file: file containing training data
      test_file: file containing testing data
    """
    self.k = k
    self.dist_function = dist_function
    self.unitw = unitw
    self.train_file = train_file
    self.test_file = test_file

  def run(self):
    """Run the data-processing, training, testing and printing
    phases of the classifier.
    """
    self.prepare_data()
    self.train()
    self.test()
    self.print_metrics()

  def prepare_data(self):
    """Prepare training and testing data"""
    self.prepare_train_data()
    self.prepare_test_data()

  def prepare_train_data(self):
    """Prepare the training data from the file"""
    df = pd.read_csv(self.train_file, header=None)
    self.train_data = df[df.columns[:-1]].to_numpy()
    self.train_labels = df[df.columns[-1]].to_numpy()

  def prepare_test_data(self):
    """Prepare the testing data from the file"""
    df = pd.read_csv(self.test_file, header=None)
    self.test_data = df[df.columns[:-1]].to_numpy()
    self.test_labels = df[df.columns[-1]].to_numpy()

  def train(self):
    """Training phase of the classifier."""
    pass

  def find_knn_indices(self, y):
    """Find the indices of the k nearest neighbors
    of a test feature"""
    distances = []
    for idx, x in enumerate(self.train_data):
      distance = self.dist_function(x, y)
      vote_weight = 1 if self.unitw else 1/max(distance, 0.0001)
      distances.append((distance, idx, vote_weight))
    distances.sort()
    return distances[:self.k]

  def test(self):
    """Testing phase of the classifier"""
    self.predicted_labels = []
    for y in self.test_data:
      knn_indices = self.find_knn_indices(y)
      label_scores = {}
      for data in knn_indices:
        label = self.train_labels[data[1]]
        vote_weight = data[2]
        if label in label_scores:
          label_scores[label] += vote_weight
        else:
          label_scores[label] = vote_weight
      predicted_label = max(label_scores, key=label_scores.get)
      self.predicted_labels.append(predicted_label)

  def print_metrics(self):
    for gt, p in zip(self.test_labels, self.predicted_labels):
      print(f"want={gt} got={p}")

    precision_dict = defaultdict(lambda : {"predicted_count": 0, "actual_count": 0})
    recall_dict = defaultdict(lambda : {"predicted_count": 0, "actual_count": 0})
    for gt, p in zip(self.test_labels, self.predicted_labels):
      if p == gt:
        precision_dict[p]["predicted_count"] += 1
        precision_dict[p]["actual_count"] += 1
        recall_dict[gt]["predicted_count"] += 1
        recall_dict[gt]["actual_count"] += 1
      else:
        precision_dict[p]["predicted_count"] += 1
        recall_dict[gt]["actual_count"] += 1

    labels = set(self.test_labels) | set(self.predicted_labels)
    for label in sorted(labels):
      precision_data = precision_dict[label]
      recall_data = recall_dict[label]
      print(f"Label={label} "
            f"Precision={precision_data['actual_count']}/{precision_data['predicted_count']} "
            f"Recall={recall_data['predicted_count']}/{recall_data['actual_count']}")

class KMeans(Classifier):
  """The K-Means classifier"""
  def __init__(self, dist_function, data_file, centroids):
    """The K Means clustering based classifier

    Args:
      dist_function: distance function to calculate closeness of neighbors.
      data_file: file containing the data to be clustered.
      centroids: initial centroid values/features to start the clustering.
    """
    self.dist_function = dist_function
    self.data_file = data_file
    self.centroids = []
    for c in centroids:
      feats = c.split(",")
      feats = [float(f) for f in feats]
      self.centroids.append(feats)
    self.k = len(self.centroids)

  def run(self):
    """Run the data-processing, training, testing and printing
    phases of the classifier.
    """
    self.prepare_data()
    self.train()
    self.test()
    self.print_metrics()

  def prepare_data(self):
    """Prepare the training data from the file"""
    df = pd.read_csv(self.data_file, header=None)
    self.train_data = df[df.columns[:-1]].to_numpy()
    self.train_labels = df[df.columns[-1]].to_numpy()

  def find_nearest_centroid(self, x):
    """Find the centroid which is nearest to the datapoint"""
    distances = []
    for idx, c in enumerate(self.centroids):
      distance = self.dist_function(x, c)
      distances.append((distance, idx))
    distances.sort()
    return distances[0]

  def get_new_centroids(self):
    """Calculate the new centroids based on the clusters"""
    new_centroids = []
    self.clusters = defaultdict(list)
    for x, label in zip(self.train_data, self.train_labels):
      _, centroid_idx = self.find_nearest_centroid(x)
      self.clusters[centroid_idx].append((x, label))

    for i in range(self.k):
      if len(self.clusters[i]) == 0:
        centroid = self.centroids[i]
      else:
        point_data = [p[0] for p in self.clusters[i]]
        centroid = np.mean(np.array(point_data), axis=0)
      new_centroids.append(centroid)
    return new_centroids

  def is_converged(self, new_centroids, old_centroids):
    """Check if the clusters have converged"""
    for nc, oc in zip(new_centroids, old_centroids):
      for i,j in zip(nc, oc):
        if i!=j:
          return False
    return True

  def train(self):
    """Training phase of the classifier."""
    new_centroids = self.get_new_centroids()
    while not self.is_converged(new_centroids, self.centroids):
      self.centroids = new_centroids
      new_centroids = self.get_new_centroids()

  def print_metrics(self):
    print("CENTROIDS")
    for i in range(self.k):
      print(f"C{i+1} = {self.centroids[i]}")

    print("ASSOCIATIONS")
    for i in range(self.k):
      points = [p[1] for p in self.clusters[i]]
      print(f"C{i+1} = {points}")

  def test(self):
    """Testing phase of the classifier"""

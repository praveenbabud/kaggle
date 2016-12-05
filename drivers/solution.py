import numpy as np
from sklearn.cluster import MeanShift as ms
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt

centers = [[1,1], [5,5]]

X, y = make_blobs(n_samples=200, centers = centers, cluster_std=1)

plt.scatter(X[:,0], X[:,1])
plt.show()

ms.fit(X)
labels = ms.labels_
cluster_centers = ms.clusters_centers_

n_clusters_ = len(np.unique(labels))

print("Number of estimated clusters:", n_clusters_)



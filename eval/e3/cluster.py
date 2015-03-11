#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import numpy as np
from numpy import loadtxt
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
from matplotlib import pyplot as plt


''' K-Means params. '''
CLUSTERS = 3
KMEANS_RUNS = 30  # Set to a value for pseudo-deterministic clusters
TOP_FEATURES = 5

''' MDS params. '''
MDS_START_STATE = 1

DATA = 'answer_features.csv'
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)


def main():
    ''' Adapted from tutorial at http://brandonrose.org/clustering#K-means-clustering. '''

    ''' Get answers and number of columns. '''
    answer_ids = []
    feat_names = []
    with open(DATA) as d:
        ncols = len(d.readline().split(','))
    with open(DATA) as d:
        for name in d.readline().split(',')[1:]:
            answer_ids.append(name)
    with open(DATA) as d:
        for line in d.readlines():
            feat_names.append(line.split(',')[0])
        feat_names = feat_names[1:]

    ''' Read data into TF-IDF matrix. '''
    data = loadtxt(DATA, dtype=str, delimiter=',', usecols=range(1, ncols), skiprows=1)
    data = (data == 'TRUE').astype(float)
    for row in data:
        if sum(row) > 0:
            row /= sum(row)
    data = data.T

    ''' Perform K-Means on the samples. '''
    kmeans = KMeans(n_clusters=CLUSTERS, n_init=KMEANS_RUNS)
    kmeans.fit(data)
    clusters = kmeans.labels_.tolist()
    
    print "=== CLUSTER MEMBERS ==="
    cluster_members = {}
    for i, c in enumerate(clusters):
        if c not in cluster_members:
            cluster_members[c] = []
        cluster_members[c].append(i)
    for cid, group in cluster_members.items():
        print "Cluster %d: %s" % (cid, str([int(answer_ids[i]) for i in group]))
    print

    print "=== FEATURES ==="
    answers = {'id': answer_ids, 'cluster': clusters}
    frame = pd.DataFrame(answers, index=[clusters])
    centroid_feats = kmeans.cluster_centers_.argsort()[:, ::-1]
    for i, centroid in enumerate(centroid_feats):
        print "Cluster %d: " % i,
        for feat in centroid[:TOP_FEATURES]:
            print feat_names[feat] + ",",
        print
    print

    ''' Do MDS so we can plot the clusters spatially. '''
    mds = MDS(random_state=MDS_START_STATE)
    pos = mds.fit_transform(data)
    xs, ys = pos[:, 0], pos[:, 1]
    cluster_colors = {0: '#e7298a', 1: '#d95f02', 2: '#7570b3'}
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))
    groups = df.groupby('label')
    fig, ax = plt.subplots(figsize=(17, 9))
    ax.margins(0.05)
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', color=cluster_colors[name], ms=12, mec='none')
        ax.set_aspect('auto')
        ax.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        ax.tick_params(axis='y', which='both', left='off', right='off', labelleft='off')
    plt.show()

    ''' Check quality of MDS, through plot and correlations '''
    dist_orig = euclidean_distances(data, data).flatten()
    dist_subseq = euclidean_distances(pos, pos).flatten()
    fig, ax = plt.subplots(figsize=(17, 9))
    ax.margins(0.05)
    ax.plot(dist_orig, dist_subseq, marker='o', linestyle='')
    plt.show()


if __name__ == '__main__':
    main()

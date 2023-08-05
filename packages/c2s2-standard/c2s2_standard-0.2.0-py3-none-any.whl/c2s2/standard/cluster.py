import numpy as np

from c2s2.base.cluster import ClusteringAlgorithm
from sklearn.cluster import AgglomerativeClustering, SpectralClustering as SklearnSpectralClustering


class HierachicalClustering(ClusteringAlgorithm):
    def cluster(self, similarity_matrix, k_clusters) -> np.ndarray:
        """Cluster the similarity matrix
        :param similarity_matrix: the similarity matrix of the patients to cluster
        :param k_clusters: the number of clusters to form
        """
        clusterer = AgglomerativeClustering(n_clusters=k_clusters, affinity='precomputed', linkage='single')
        #AgglomerativeClustering  implementation needs distance matrix, we have similarity, so lets flip distribution
        distance_matrix = np.max(similarity_matrix) - similarity_matrix
        clusterer.fit(distance_matrix)
        return clusterer.labels_


class SpectralClustering(ClusteringAlgorithm):
    def cluster(self, similarity_matrix, k_clusters) -> np.ndarray:
        """Cluster the similarity matrix
        :param similarity_matrix: the similarity matrix of the patients to cluster
        :param k_clusters: the number of clusters to form
        """
        clusterer = SklearnSpectralClustering(n_clusters=k_clusters, affinity='precomputed')
        clusterer.fit(similarity_matrix)
        return clusterer.labels_


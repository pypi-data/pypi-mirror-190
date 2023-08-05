import typing

import numpy as np

from c2s2.base.cluster import ClusteringAlgorithm
from c2s2.base.model import Sample
from c2s2.base.perturb import Perturbation
from c2s2.base.semsim import SimilarityMatrixCreator
from ._base import ConsensusClustering


class SimpleConsensusClustering(ConsensusClustering):

    def __init__(self, k_clusters, n_resample,
                 sim_matrix_creator: SimilarityMatrixCreator,
                 perturb_method: Perturbation,
                 clustering_algorithm: ClusteringAlgorithm,
                 pac_threshold: typing.Tuple[float, float] = (.1, .9)):
        """Constructor

        :param k_clusters: the upper limit of the clusters to investigate. The limit is included
        :param n_resample: number of times to resample/pertube the dataset
        :param sim_matrix_creator: the similarity matrix creator to calculate the phenotypic similarity matrix
                for patients
        :param perturb_method: the method to resample/perturb the input data for consensus clustering
        :param clustering_algorithm: the algorithm to cluster the patient data, i.e. KMeans, DBScan, etc
        :param pac_threshold: threshold values for determining the proportion of ambiguously clustered samples
                            The thresholds must be a sequence of two floats that are in range [0, 1].
        """
        if k_clusters < 2:
            raise ValueError(f"`k_clusters` {k_clusters} must be greater than 1")

        self._k_clusters = list(range(2, k_clusters + 1))
        self._n_resample = n_resample
        # TODO verify properties of sim_kernel, perturb_method, clustering_algorithm
        self._sim_matrix_creator = sim_matrix_creator
        self._perturb_method = perturb_method
        self._clustering_algorithm = clustering_algorithm
        if not isinstance(pac_threshold, typing.Sequence) or len(pac_threshold) != 2:
            raise ValueError(f'`pac_threshold` {pac_threshold} must be a sequence of 2 items')
        if pac_threshold[0] >= pac_threshold[1]:
            raise ValueError(f'Lower `pac_threshold` bound {pac_threshold[0]} must be less than the upper bound {pac_threshold[1]}')
        if not all([0 <= val <= 1 for val in pac_threshold]):
            raise ValueError(f'`pac_threshold` values {pac_threshold} must be in range [0, 1]')
        self._pac_threshold = pac_threshold

        self._sim_matrix_original = None
        self._labels = None
        self._connectivity_matrix = None
        self._pac = None
        self._p_values = None

    def consensus_cluster(self, samples: typing.Sequence[Sample]):
        M = np.zeros((len(self._k_clusters), len(samples), len(samples)), dtype=float)
        clustering_labels = []
        self._sim_matrix_original = self._sim_matrix_creator.calculate_matrix(samples)

        pac_rand = np.zeros((len(self._k_clusters), 1000))

        # Try the desired cluster numbers
        for i, k in enumerate(self._k_clusters):
            clusters_original_data = self._clustering_algorithm.cluster(self._sim_matrix_original, k)
            clustering_labels.append(clusters_original_data)

            # Perturb dataset and run clustering algorithm
            total_it = len(self._k_clusters) * self._n_resample
            for h in range(self._n_resample):
                perturbed = self._perturb_method.perturb(samples)
                similarity_matrix = self._sim_matrix_creator.calculate_matrix(perturbed)
                clusters = self._clustering_algorithm.cluster(similarity_matrix, k)
                M[i, :, :] = M[i, :, :] + np.array([clusters == a for a in clusters], dtype=int)
                x = int(100 * (self._n_resample * i + h) / total_it)
                print(f"Consensus clustering :[{u'█' * x}{('.' * (100 - x))}] {(self._n_resample * i + h)}/{total_it}",
                      end='\r', flush=True)

            # For every cluster, calculate random PAC scores as well to compare them to actual PAC later
            avg_clusters = np.mean(clusters)
            if avg_clusters < 0.1:
                avg_clusters = 0.1
            elif avg_clusters > 0.9:
                avg_clusters = 0.9
            for z in range(pac_rand.shape[1]):
                pac_temp = np.zeros((len(samples), len(samples)), dtype=float)
                for h in range(self._n_resample):
                    clusters_shuffled = np.random.binomial(n=1, p=avg_clusters, size=len(clusters))
                    clusters_shuffled_count = np.array([clusters_shuffled == a for a in clusters_shuffled], dtype=int)
                    pac_temp = pac_temp + clusters_shuffled_count
                pac_temp = pac_temp / self._n_resample
                pac_rand[i, z] = np.mean((pac_temp > self._pac_threshold[0]) & (pac_temp < self._pac_threshold[1]))
        self._connectivity_matrix = M / self._n_resample
        self._pac = np.mean(
            (self.connectivity_matrix > self._pac_threshold[0]) & (self.connectivity_matrix < self._pac_threshold[1]),
            axis=(1, 2))
        p_values = np.zeros(len(self._k_clusters))
        for i in range(len(self._k_clusters)):
            p_values[i] = np.mean(self._pac[i] > pac_rand[i, :])
        self._p_values = p_values
        self._labels = clustering_labels

        return self

    #############
    # Properties

    @property
    def connectivity_matrix(self) -> typing.Optional[np.ndarray]:
        return self._connectivity_matrix
    @property
    def p_values(self) -> typing.Optional[np.ndarray]:
        return self._p_values

    @property
    def pac(self) -> typing.Optional[np.ndarray]:
        return self._pac

    @property
    def k_clusters(self) -> typing.Optional[typing.Sequence[int]]:
        return None if self._connectivity_matrix is None else self._k_clusters

    @property
    def labels(self) -> typing.Optional[np.ndarray]:
        return self._labels

    @property
    def sim_matrix_original(self) -> typing.Optional[np.ndarray]:
        return self._sim_matrix_original

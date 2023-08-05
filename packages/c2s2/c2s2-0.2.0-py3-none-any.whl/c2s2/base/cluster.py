import abc
import sys
import warnings

import numpy as np

warnings.filterwarnings('ignore')


class ClusteringAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def cluster(self, similarity_matrix: np.ndarray, k_clusters: int) -> np.ndarray:
        """
        Cluster the similarity matrix.

        Parameters
        ----------
        similarity_matrix : array of shape (n_samples, n_samples) with similarities between samples to cluster.
        k_clusters        : the number of clusters to form

        Returns
        -------
        y : ndarray of shape (n_samples,) with indices of sample cluster membership.
        """
        pass


class KMeans(ClusteringAlgorithm):
    """
     Perform K-means clustering starting from a similarity (kernel) matrix.
     This type of K-means clustering is not supported out of the box by scikit learn.
     The code was developed for use in the N3C platform.
     """
    # from https://github.com/National-COVID-Cohort-Collaborative/kernelkm/blob/master/src/kernelkm/kernel_k_means.py

    def __init__(self, max_iter=100_000):
        """
        max_iter: a positive int for the maximum number of iteration to do when refining clusters [10,000]
        """
        if not isinstance(max_iter, int):
            raise ValueError(f"max_iter must be an int but was {type(max_iter)}")
        if max_iter <= 0:
            raise ValueError(f"max_iter must be a positive int but was {max_iter}")

        self._max_iter = max_iter
        self._matrix = None

    def cluster(self, similarity_matrix: np.ndarray, k_clusters: int):
        """Run k means clustering for the given k (number of clusters)
        datamat: a symmetric matrix (as a numpy array) with patient-patient similarities

        """
        if not isinstance(similarity_matrix, np.ndarray):
            raise ValueError("datamat parameter needs to be an np.ndarray")
        if similarity_matrix.ndim != 2:
            raise ValueError("datamat parameter needs to be 2 dimensional array")
        shape = similarity_matrix.shape
        if shape[0] != shape[1]:
            raise ValueError("datamat needs to be a square matrix")

        if not isinstance(k_clusters, int) or k_clusters < 2:
            raise ValueError("Must call this function with one argument - an integer k for the number of clusters")
        centroids = self._plus_plus(k_clusters, similarity_matrix)  # _init_centroids(k)
        errors = []
        i = 0

        while True:
            centroid_assignments, centroid_errors = self._assign_to_centroid(similarity_matrix, centroids)
            errors.append(centroid_errors)
            centroids_new = self._adjust_centroids(similarity_matrix, centroid_assignments)
            if np.array_equal(centroids, centroids_new):
                break
            else:
                centroids = centroids_new
            i += 1
            if i == self._max_iter:
                print(f"Reaching maximum allowed iterations ({self._max_iter}), terminating optimization loop")
                break
        return np.array(centroid_assignments, dtype=int)

    @staticmethod
    def _plus_plus(k, similarity_matrix: np.ndarray):
        """Create cluster centroids using the k-means++ algorithm.

        This method makes an effort to choose centroids that are far apart from one another when initializing
        the clustering. This in theory reduces the chance of very bad clustering that results from poorly chosen
        initial centroids. Inspiration from here:
        https://stackoverflow.com/questions/5466323/how-could-one-implement-the-k-means-algorithm

        Parameters
        ----------
        k : int
            The desired number of clusters for which centroids are required.
        similarity_matrix : numpy array
            The dataset to be used for centroid initialization.
        Returns
        -------
        centroids : numpy array
            Collection of k centroids as a numpy array.
        """

        centroids = [similarity_matrix[0]]

        for _ in range(1, k):
            dist_sq = np.array([min([np.inner(c - x, c - x) for c in centroids]) for x in similarity_matrix])
            probs = dist_sq / dist_sq.sum()
            cumulative_probs = probs.cumsum()
            r = np.random.rand()

            i = None
            for j, p in enumerate(cumulative_probs):
                if r < p:
                    i = j
                    break

            # The above loop should ALWAYS set `i` since `r` is a value between 0 and 1.
            # The only EXCEPTION is when all entries of the similarity matrix are `0.`.
            # This should not happen in practice, but can happen if we cluster samples that only have
            # `HP:0000001` (All) in phenotypic features.
            #
            # Cumulative_probs is a cumsum, the last entry is therefore always 1, so the last entry (`p` below)
            # in cumulative_probs is always larger than `r`.
            # Anyway, we check to make the compiler happy and guard against unexpected situations.
            if i is None:
                raise ValueError("Uninitialized index. Please report to the developers.")

            centroids.append(similarity_matrix[i])
        return np.array(centroids)

    @staticmethod
    def _init_centroids(matrix, k):
        """
        initialize centroids to uniform random values between the minimum (0.0) and maximum of all similarity values
        """
        centroid_min = 0.0
        centroid_max = matrix.max().max()
        n = len(matrix)
        centroids = []  # a list of np.ndarray's
        for centroid in range(k):
            centroid = np.random.uniform(centroid_min, centroid_max, n)
            centroids.append(centroid)
            if n != len(centroid):
                raise ValueError("Problem constructing centroid")
        return np.array(centroids)

    @staticmethod
    def _assign_to_centroid(matrix, centroids):
        n_patients = len(matrix)
        centroids_assigned = []
        centroid_errors = []
        k = len(centroids)

        for pat in range(n_patients):
            min_centroid_error = sys.float_info.max
            closest_centroid_idx = -1
            for centroid in range(k):
                # centroids.iloc retrieves a pandas series
                # and seld._matrix[pat, :] retrieves a ndarray
                # both represent vectors of similarities
                patient_a = centroids[centroid, :]
                patient_b = matrix[pat, :]
                if len(patient_a) != len(patient_b):
                    raise ValueError(
                        f"Unqual lengths - centroid {centroid}: {len(patient_a)} and patient {pat}: {len(patient_b)}")
                error = np.sqrt(np.sum((patient_a - patient_b) ** 2))
                if error < min_centroid_error:
                    min_centroid_error = error
                    closest_centroid_idx = centroid
            if closest_centroid_idx < 0:
                #  if this happens, there is probably an error that the user needs to know about
                #  and so we should stop execution.
                raise ValueError(f"Failed to assign patient {pat} to centroid (should never happen)")
            centroids_assigned.append(closest_centroid_idx)
            centroid_errors.append(min_centroid_error)

        return centroids_assigned, centroid_errors

    @staticmethod
    def calculate_sse(matrix, centroids, centroid_assignments):
        """Calculates the SSE for a given clustering

        The SSE is the sum of the square of the Euclidean distance from each data points (here a
        patient) to the centroid of the cluster to which the data point has been assigned.
        """
        n_patients = len(matrix)
        sse = 0
        for pat_idx in range(n_patients):
            c = centroid_assignments[pat_idx]
            assigned_centroid = centroids.iloc[c, :].to_numpy()
            patient_vector = matrix[pat_idx, :]
            error = np.sum((assigned_centroid - patient_vector) ** 2)
            sse += error
        return sse

    @staticmethod
    def _adjust_centroids(matrix, centroid_assignments):
        """
        centroid_assignments - a list of integers with the same length as the number of patients
                               each entry represents the centroid to which the patient has been assigned
        return - a DataFrame with the new centroids that correspond to the patient assignments.
        """
        if not isinstance(centroid_assignments, list):
            raise ValueError("centroids argument must be a list")
        centroid_assignments = np.array(centroid_assignments)

        new_centroids = []
        for centroid in np.unique(centroid_assignments):
            new_centroids.append(matrix[centroid_assignments == centroid, :].mean(axis=0))
        return np.array(new_centroids, dtype=int)

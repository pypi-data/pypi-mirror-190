import abc
import typing

import numpy as np

from c2s2.base.model import Sample


class ConsensusClustering(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def consensus_cluster(self, samples: typing.Sequence[Sample]):
        pass

    @property
    @abc.abstractmethod
    def connectivity_matrix(self) -> typing.Optional[np.ndarray]:
        """
        Get connectivity matrix.

        The matrix is a symmetric :math:`[n\\ x\\ n]` matrix where :math:`n` is
        the number of samples used for fitting. The row/column order corresponds to the order of samples submitted
        for clustering.

        :return: an array with connectivity matrix or `None` if the clusterer has not yet been fitted.
        """
        pass

    @property
    @abc.abstractmethod
    def pac(self) -> typing.Optional[np.ndarray]:
        """
        Get an array with proportion of ambiguously clustered.

        :return: the `pac` array or `None` if the clusterer has not yet been fitted.
        """
        pass

    @property
    @abc.abstractmethod
    def k_clusters(self) -> typing.Optional[typing.Sequence[int]]:
        """
        Get a sequence of cluster count that has been fitted.
        The count corresponds to the 0th axis of `self.connectivity_matrix`.

        :return: a sequence of cluster count or `None` if the clusterer has not yet been fitted.
        """
        pass

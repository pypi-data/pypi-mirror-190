import numpy as np

from c2s2.base.model import Sample
from ._base import SimilarityKernel


class DummySimilarityKernel(SimilarityKernel):
    """A dummy similarity kernel that returns a random similarity value in range [0, 1]."""

    def compute(self, patient_a: Sample, patient_b: Sample) -> float:
        return np.random.uniform(0, 1)

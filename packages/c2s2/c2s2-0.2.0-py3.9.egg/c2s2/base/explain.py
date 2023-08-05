import abc
from c2s2.base.model import Sample, PhenotypicFeature
import numpy as np
import typing
import math


class ExplainMethod(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def explain(self, samples: typing.Sequence[Sample], cluster_labels: np.ndarray) -> typing.Tuple[
        typing.List[PhenotypicFeature], np.ndarray, float]:
        """
        Detect and explain the differences between determined clusters

        Parameters
        ----------
        samples : the samples to detect the difference for
        cluster_labels: the determined labels of the clusters
        hpo_graph: the HPO graph in networkx format
        Returns
        -------
        sig_features: phenotypic features that are statistically significantly different bewteen clusters
        np_contingency_sig: 3D array which contains the contigency matrices for the significant features.
        Dimensions are (number of HPO terms, 2 (positive and negative row), number of clusters)
        p_threshold: threshold used for significance
        """
        pass


def fisher_freeman_halton(n: np.ndarray) -> dict:
    """Perform the Fisher-Freeman-Halton test on a contigencytable of rxc

      This is a port of the implementation in R of the contingencytables library, see
      https://search.r-project.org/CRAN/refmans/contingencytables/html/FisherFreemanHalton_asymptotic_test_rxc.html"
      This port was almost entirely done by ChatGPT, see https://chat.openai.com/chat

      samples : the samples to detect the difference for
      cluster_labels: the determined labels of the clusters
      hpo_graph: the HPO graph in networkx format
    """
    r, c = n.shape
    nip = np.sum(n, axis=1)
    npj = np.sum(n, axis=0)
    N = np.sum(n)

    # Point probability of the observed table
    f = multiple_hypergeometric_pdf(n, N, r, c, nip, npj)

    N_float = float(N)
    N_CALC = (N_float ** (-((r * c) - 1)))

    # need some object array below, because when using default numpy, overflows occur
    gamma = math.sqrt(
        ((2 * math.pi) ** ((r - 1) * (c - 1))) * N_CALC * np.prod(np.array(nip ** (c - 1), dtype=object))
        * np.prod(np.array(npj ** (r - 1), dtype=object)))
    if (np.sum(npj == 0) > 0):
        gamma = 1

    # Test statistic and P-value from the chi-squared distribution with
    # (r-1)(c-1) degrees of freedom
    T0 = -2 * np.log(gamma * f)
    df = int((r - 1) * (c - 1))

    # below is calculation without scipy
    x = np.random.chisquare(df, size=1000000)
    # Count the number of random variables that are greater than T0
    greater_than_t0 = np.sum(x > T0)
    # Compute the P-value as the fraction of random variables that are greater than T0
    P = greater_than_t0 / x.size

    return {"p": P, "t": T0, "df": df}


def multiple_hypergeometric_pdf(x, N, r, c, nip, npj) -> float:
    if (np.max(x) > 170).any() or (np.max(nip) > 170) or (np.max(npj) > 170):
        return np.nan

    # Somewhat messy code to avoid overflow
    if N > 170:
        cutoff = 170
    else:
        cutoff = math.floor(N / 2)
    Nfact1 = math.factorial(cutoff)
    Nfact2 = 1
    for i in range(cutoff + 1, N + 1):
        Nfact2 *= i
    # using arrays of type object here, because when using int64, for larger contingency tables, overflows happen
    terms1 = np.array([math.factorial(npj_i) for npj_i in npj], dtype=object)
    terms2 = np.array([math.factorial(nip_i) for nip_i in nip], dtype=object)
    f = 1 / Nfact1
    f *= terms1[0]
    f *= np.prod(terms1[1:])
    f /= Nfact2
    f *= terms2[0]
    f *= np.prod(terms2[1:])
    for i in range(r):
        for j in range(c):
            f /= math.factorial(x[i, j])
    return f

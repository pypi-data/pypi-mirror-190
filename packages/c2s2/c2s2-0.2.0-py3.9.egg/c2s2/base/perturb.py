import abc
import copy
import typing

import itertools

import numpy as np

from c2s2.base.model import TermId, Phenotyped
from c2s2.base.model.simple import SimplePhenotypicFeature
from .semsim import SimilarityMatrixCreator


class Perturbation(metaclass=abc.ABCMeta):
    """
    Perturb the input sequence of `Phenotyped` samples.

    Attributes:
        P    Generic type to constrain items we can perturb to implementors of :class:`c2s2.base.model.Phenotyped`.
    """

    P = typing.TypeVar('P', bound=Phenotyped)

    @abc.abstractmethod
    def perturb(self, samples: typing.Sequence[P]) -> typing.Sequence[P]:
        # here perturb patient_data as part of consensus clustering to obtain stability of clusters
        pass


class NoPerturbation(Perturbation):
    """
    Dummy perturbation that does nothing with the input.
    """

    def perturb(self, samples: typing.Sequence[Perturbation.P]) -> typing.Sequence[Perturbation.P]:
        """
        No-op that returns the input sequence
        """
        return samples


class IncompletePhenotyping(Perturbation):
    """
    Incomplete phenotyping downsamples each sample to n phenotypic features.
    """

    def __init__(self, number_of_terms_per_patient: int):
        """Constructor
        :param number_of_terms_per_patient: number of HPO terms to downsample each individual to
        """
        if number_of_terms_per_patient <= 0:
            raise ValueError(f'Number of terms per patient {number_of_terms_per_patient} must be greater than 0')
        self._number_of_terms_per_patient = number_of_terms_per_patient

    def perturb(self, samples: typing.Sequence[Perturbation.P]) -> typing.Sequence[Perturbation.P]:
        """
        Keep random n phenotypic features in each sample.
        """
        # execution time of this class for 131072 individuals: 1.3 seconds
        # if we decide on the data structure of patient_list, we can optimize this function by not looping over the lists of lists
        perturbed_items = np.zeros(len(samples), dtype=object)
        for i, patient in enumerate(samples):
            # only do this when number of terms is larger than number to downsample to
            if len(patient.phenotypic_features) > self._number_of_terms_per_patient:
                perturbed = copy.copy(patient)
                perturbed.phenotypic_features = np.random.choice(patient.phenotypic_features, self._number_of_terms_per_patient, replace=False)
            else:
                perturbed = patient

            perturbed_items[i] = perturbed

        return perturbed_items


class NoiseAdding(Perturbation):
    """
    Noise adding adds n random observed HPO terms to each sample.
    """

    def __init__(self, number_of_terms_to_add: typing.Union[int, float], nodes: typing.Sequence[TermId]):
        """
        :param number_of_terms_to_add: number of observed HPO terms to add as random noise to each individual.
        If float, this will be relative (i.e. 0.1 will add 10% of number of HPO terms to each individual,
        so 10 HPO terms will become 11, 20 will become 22 etc.)
        :param nodes: HPO terms to sample from to add the noise
        """
        self._hpo_terms = nodes
        if not (isinstance(number_of_terms_to_add, int) or isinstance(number_of_terms_to_add, float)):
            raise ValueError(f'Number of terms to add must be int or float but was {type(number_of_terms_to_add)}')
        if isinstance(number_of_terms_to_add, int) and number_of_terms_to_add <= 0:
            raise ValueError(f'The number of terms to add {number_of_terms_to_add} must be greater than 0')
        if isinstance(number_of_terms_to_add, float) and not 0. <= number_of_terms_to_add <= 1.:
            raise ValueError(f'The ratio of terms to add {number_of_terms_to_add} must be in [0, 1]')

        self._number_of_terms_to_add = number_of_terms_to_add

    def perturb(self, samples: typing.Sequence[Perturbation.P]) -> typing.Sequence[Perturbation.P]:
        """Add a certain number of random/noise terms into each patient
        :param samples: could be a dataframe with a column of HPO ids as lists, a spark dataframe, phenopackets, etc
        """
        # Use an array to do a single allocation.
        perturbed_items = np.zeros(len(samples), dtype=object)

        for i, patient in enumerate(samples):
            perturbed = copy.copy(patient)
            hpo_terms_needed = self._number_of_terms_to_add \
                if isinstance(self._number_of_terms_to_add, int) \
                else int(np.round(len(patient.phenotypic_features) * self._number_of_terms_to_add))

            selected_hpos = [
                SimplePhenotypicFeature(term_id, status=True)
                for term_id in np.random.choice(self._hpo_terms, size=hpo_terms_needed)
            ]

            pfs = list(itertools.chain(perturbed.phenotypic_features, selected_hpos))
            perturbed.phenotypic_features = pfs
            perturbed_items[i] = perturbed

        return perturbed_items


class DecreaseSimilarityByRatio(Perturbation):
    def __init__(self, ratio_of_similarity, sim_matrix_creator: SimilarityMatrixCreator):
        """Constructor
        :param ratio_of_similarity: ratio to target, i.e. if 0.9, stop when the mean of the similarity matrix is 0.9
        :param sim_matrix_creator: the similarity matrix creator to calculate the phenotypic similarity matrix
        for patients
        """
        self._ratio_of_similarity = ratio_of_similarity
        if not isinstance(sim_matrix_creator, SimilarityMatrixCreator):
            raise ValueError(f'sim_matrix_creator must be an instance of SimilarityMatrixCreator but was {type(sim_matrix_creator)}')
        self._sim_matrix_creator = sim_matrix_creator

    def perturb(self, patient_list):
        """Perturb the input data
        :param patient_list: could be a dataframe with a column of HPO ids as lists, a spark dataframe, phenopackets, etc
        """
        new_patient_list = patient_list[:]
        curr_similarity = self._sim_matrix_creator.calculate_matrix(new_patient_list).mean()
        target_similarity = curr_similarity * self._ratio_of_similarity
        while True:
            new_patient_list_temp = []
            for l in new_patient_list:
                if len(l) > 1:
                    new_patient_list_temp.append(random.sample(l, len(l) - 1))
                else:
                    new_patient_list_temp.append(l)
            new_patient_list = new_patient_list_temp[:]
            if np.mean([len(l) for l in new_patient_list]) == 1:
                # all individuals only have one HPO term left, no sense in continuing
                break
            curr_similarity = self._sim_matrix_creator.calculate_matrix(new_patient_list).mean()
            if curr_similarity < target_similarity:
                break
        return new_patient_list

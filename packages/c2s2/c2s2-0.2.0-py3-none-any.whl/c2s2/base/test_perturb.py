import unittest
import numpy as np

from c2s2.base.model import TermId, Sample
from c2s2.base.model.simple import SimpleSample, SimplePhenotypicFeature
from .perturb import NoiseAdding, IncompletePhenotyping, NoPerturbation


def make_clustering_item(identifier: str, pfs) -> Sample:
    features = [SimplePhenotypicFeature(TermId.of(term), status=True) for term in pfs]
    return SimpleSample(identifier=identifier, phenotypic_features=features)


class PerturbationTester(unittest.TestCase):

    def setUp(self):
        self._random_patient_list = [
            make_clustering_item('A', ['HP:0001166', 'HP:0002266', 'HP:0011682', 'HP:0001433', 'HP:0032648',
                                       'HP:0004878', 'HP:0010677', 'HP:0001257', 'HP:0006280']),
            make_clustering_item('B', ['HP:0002266', 'HP:0011682', 'HP:0032648', 'HP:0004878', 'HP:0001257']),
            make_clustering_item('C', ['HP:0001166', 'HP:0032648', 'HP:0004878', 'HP:0010677']),
            make_clustering_item('D', ['HP:0001166', 'HP:0002266', 'HP:0032648', 'HP:0004878', 'HP:0010677',
                                       'HP:0001257', 'HP:0006280']),
            make_clustering_item('E', ['HP:0001433', 'HP:0032648', 'HP:0004878', 'HP:0010677', 'HP:0001257']),
            make_clustering_item('F', ['HP:0001166', 'HP:0011682', 'HP:0004878', 'HP:0010677', 'HP:0006280']),
            make_clustering_item('G', ['HP:0001166', 'HP:0011682', 'HP:0032648', 'HP:0010677', 'HP:0006280']),
            make_clustering_item('H', ['HP:0002266'])
        ]

    def test_no_perturbation(self):
        perturber = NoPerturbation()
        assert (self._random_patient_list == perturber.perturb(self._random_patient_list))

    def test_noise_adding(self):
        fake_hp_nodes = [TermId.of(f"HP:{str(tid).rjust(7, '0')}") for tid in range(20)]
        perturber = NoiseAdding(number_of_terms_to_add=5, nodes=fake_hp_nodes)
        current_length_plus_five = [len(a.phenotypic_features) + 5 for a in self._random_patient_list]
        new_length = [len(a.phenotypic_features) for a in perturber.perturb(self._random_patient_list)]
        assert (new_length == current_length_plus_five)

    def test_noise_adding_relative(self):
        fake_hp_nodes = [TermId.of(f"HP:{str(tid).rjust(7, '0')}") for tid in range(10)]
        perturber = NoiseAdding(number_of_terms_to_add=.2, nodes=fake_hp_nodes)
        current_length_plus_ten_percent = [int(np.round(len(a.phenotypic_features) * 1.2)) for a in self._random_patient_list]
        new_length = [len(a.phenotypic_features) for a in perturber.perturb(self._random_patient_list)]
        assert (new_length == current_length_plus_ten_percent)

    def test_incomplete_phenotyping(self):
        downsample_to = 5
        perturber = IncompletePhenotyping(number_of_terms_per_patient=downsample_to)
        expected = [min(downsample_to, len(patient.phenotypic_features)) for patient in self._random_patient_list]
        actual = [len(a.phenotypic_features) for a in perturber.perturb(self._random_patient_list)]
        self.assertListEqual(actual, expected)

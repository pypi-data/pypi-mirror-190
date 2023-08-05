import os
import unittest

import networkx as nx
from pkg_resources import resource_filename

from c2s2.base.model import TermId
from c2s2.base.model.simple import SimpleSample, SimplePhenotypicFeature
from .load_hpo_graph import get_hpo_graph_in_networkx
from .perturb import Imprecision, NLevelsUpImprecision

local_hpo = resource_filename(__name__, os.path.join('test_data', 'hp.toy.json'))


# The available leaf nodes:
# [
#  'HP:0001166', 'HP:0002266', 'HP:0011682', 'HP:0001433', 'HP:0032648',
#  'HP:0004878', 'HP:0010677', 'HP:0001257', 'HP:0006280'
# ]


def make_clustering_item(identifier: str, pfs) -> SimpleSample:
    features = [SimplePhenotypicFeature(TermId.of(term), status=True) for term in pfs]
    return SimpleSample(identifier=identifier, phenotypic_features=features)


class TestPerturb(unittest.TestCase):

    def setUp(self) -> None:
        self._random_patient_list = [
            make_clustering_item('A', ['HP:0001166', 'HP:0002266', 'HP:0011682', 'HP:0001433', 'HP:0032648',
                                       'HP:0004878', 'HP:0010677', 'HP:0001257', 'HP:0006280']),
            make_clustering_item('B', ['HP:0002266', 'HP:0011682', 'HP:0032648', 'HP:0004878', 'HP:0001257']),
            make_clustering_item('C', ['HP:0001166', 'HP:0032648', 'HP:0004878', 'HP:0010677']),
            make_clustering_item('D', ['HP:0001166', 'HP:0002266', 'HP:0032648', 'HP:0004878', 'HP:0010677',
                                       'HP:0001257', 'HP:0006280']),
            make_clustering_item('E', ['HP:0001433', 'HP:0032648', 'HP:0004878', 'HP:0010677', 'HP:0001257']),
            make_clustering_item('F', ['HP:0001166', 'HP:0011682']),
            make_clustering_item('G', ['HP:0001166', 'HP:0011682', 'HP:0032648', 'HP:0010677', 'HP:0006280']),
            make_clustering_item('H', ['HP:0002266'])
        ]

        self._hpo_graph = get_hpo_graph_in_networkx(hpo_path=local_hpo)

    def test_imprecision(self):
        perturber = Imprecision(hpo_graph=self._hpo_graph, number_of_terms_to_replace=3)
        perturbed = perturber.perturb(self._random_patient_list)

        for i in range(len(self._random_patient_list)):
            for y in range(len(self._random_patient_list[i].phenotypic_features)):
                # We only check the replaced terms
                if self._random_patient_list[i].phenotypic_features[y] != perturbed[i].phenotypic_features[y]:
                    ancestors_this_term = list(nx.ancestors(self._hpo_graph, self._random_patient_list[i].phenotypic_features[y].term_id.value))
                    assert perturbed[i].phenotypic_features[y].term_id.value in ancestors_this_term

    def test_n_levels_up(self):
        """
        Check if the ancestors are right. We only check the 6th sample with two features.
        """
        pertuber = NLevelsUpImprecision(hpo_graph=self._hpo_graph, number_of_terms_to_replace=3, level=3)
        perturbed = pertuber.perturb([self._random_patient_list[5]])

        # Due to multiple inheritance, we can get >2 ancestors that are n-level up from 2 input terms.
        expected = {'HP:0011297', 'HP:0001671', 'HP:0001155', 'HP:0001713'}
        self.assertTrue(all([pf.term_id.value in expected for pf in perturbed[0].phenotypic_features]))

    def test_n_levels_up_lengths(self):
        """
        Check if lengths are unchanged.
        """
        pertuber = NLevelsUpImprecision(hpo_graph=self._hpo_graph, number_of_terms_to_replace=3, level=3)
        # Let's check
        perturbed = pertuber.perturb(self._random_patient_list)
        expected = [len(item.phenotypic_features) for item in self._random_patient_list]
        actual = [len(item.phenotypic_features) for item in perturbed]

        self.assertListEqual(expected, actual)

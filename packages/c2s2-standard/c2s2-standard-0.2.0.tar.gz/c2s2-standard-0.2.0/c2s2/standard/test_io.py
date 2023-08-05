import os
import unittest

from pkg_resources import resource_filename

from google.protobuf.json_format import Parse
from phenopackets import Phenopacket, Cohort

from .io import read_phenopacket, read_cohort


def _read_phenopacket(json_path) -> Phenopacket:
    with open(json_path, 'r') as fh:
        return Parse(message=Phenopacket(), text=fh.read())


def _read_cohort(json_path) -> Cohort:
    with open(json_path, 'r') as fh:
        return Parse(message=Cohort(), text=fh.read())


class TestIO(unittest.TestCase):

    bethlem_myopathy_pp = resource_filename(__name__, os.path.join('test_data', 'bethlem-myopathy.json'))
    example_cohort = resource_filename(__name__, os.path.join('test_data', 'example-cohort.json'))

    def setUp(self) -> None:
        self._bm_pp = _read_phenopacket(TestIO.bethlem_myopathy_pp)
        self._cohort = _read_cohort(TestIO.example_cohort)

    def test_read_phenopacket__phenopacket(self):
        sample = read_phenopacket(self._bm_pp)
        self.assertEqual(sample.identifier, 'proband A')
        expected_pf_ids = ['HP:0001629', 'HP:0000280', 'HP:0008689', 'HP:0001561', 'HP:0000054',
                           'HP:0001798', 'HP:0001320', 'HP:0000518', 'HP:0002198', 'HP:0100333']
        actual_pf_ids = [pf.term_id.value for pf in sample.phenotypic_features]
        self.assertListEqual(expected_pf_ids, actual_pf_ids)

        # One excluded term and 9 observed
        expected_states = [False] + [True for _ in range(9)]
        actual_states = [pf.is_observed() for pf in sample.phenotypic_features]
        self.assertListEqual(expected_states, actual_states)

    def test_read_phenopacket__path(self):
        pp = read_phenopacket(TestIO.bethlem_myopathy_pp)
        self.assertIsNotNone(pp)

    def test_read_phenopacket__io_wrapper(self):
        with open(TestIO.bethlem_myopathy_pp, 'r') as fh:
            self.assertIsNotNone(read_phenopacket(fh))
        with open(TestIO.bethlem_myopathy_pp, 'rb') as fh:
            self.assertIsNotNone(read_phenopacket(fh))

    def test_parse_phenopacket__throws_on_wrong_input(self):
        with self.assertRaises(ValueError) as cm:
            read_phenopacket(self._cohort)

        self.assertEqual("Expected an argument with type <class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'> but got <class 'phenopackets.schema.v2.phenopackets_pb2.Cohort'>", cm.exception.args[0])

    def test_read_cohort__cohort(self):
        samples = read_cohort(self._cohort)

        self.assertEqual(2, len(samples))
        first = samples[0]
        self.assertEqual('cohort-member-id-1', first.identifier)
        self.assertEqual(3, len(first.phenotypic_features))

        second = samples[1]
        self.assertEqual('cohort-member-id-2', second.identifier)
        self.assertEqual(2, len(second.phenotypic_features))

    def test_read_cohort__path(self):
        cohort = read_cohort(TestIO.example_cohort)
        self.assertIsNotNone(cohort)

    def test_read_cohort__io_wrapper(self):
        with open(TestIO.example_cohort, 'r') as fh:
            self.assertIsNotNone(read_cohort(fh))
        with open(TestIO.example_cohort, 'rb') as fh:
            self.assertIsNotNone(read_cohort(fh))

    def test_parse_cohort__throw_on_wrong_input(self):
        with self.assertRaises(ValueError) as cm:
            read_cohort(self._bm_pp)

        self.assertEqual("Expected an argument with type <class 'phenopackets.schema.v2.phenopackets_pb2.Cohort'> but got <class 'phenopackets.schema.v2.phenopackets_pb2.Phenopacket'>", cm.exception.args[0])

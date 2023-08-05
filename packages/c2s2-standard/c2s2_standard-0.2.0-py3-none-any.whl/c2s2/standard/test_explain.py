import numpy as np
from c2s2.standard.explain import FisherFreemanHalton
import unittest


class ExplainabilityTester(unittest.TestCase):

    def setUp(self):
        self.explain = FisherFreemanHalton()

    def test_fisher_freeman_halton(self):
        results = self.explain._fisher_freeman_halton(np.array([[29, 11,  3,  8], [2,  1,  5,  9]]))
        self.assertAlmostEqual(results['p'], 0.000217731)
        self.assertAlmostEqual(results['t'], 19.47793, 5)
        assert(results['df'] == 3)

        results = self.explain._fisher_freeman_halton(np.array([[5, 0], [0, 5]]))
        self.assertAlmostEqual(results['p'], 0.001851743)
        self.assertAlmostEqual(results['t'], 9.690985, 5)
        assert(results['df'] == 1)

        results = self.explain._fisher_freeman_halton(np.array([[2, 4, 2, 4, 6], [3, 1, 3, 5, 7]]))
        self.assertAlmostEqual(results['p'], 0.6607656)
        self.assertAlmostEqual(results['t'], 2.410306, 5)
        assert(results['df'] == 4)
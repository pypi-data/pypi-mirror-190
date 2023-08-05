import numpy as np
from .explain import fisher_freeman_halton
import unittest


class ExplainabilityTester(unittest.TestCase):

    def test_fisher_freeman_halton(self):
        results = fisher_freeman_halton(np.array([[29, 11,  3,  8], [2,  1,  5,  9]]))
        self.assertAlmostEqual(results['p'], 0.0002, 4)
        self.assertAlmostEqual(results['t'], 19.47793, 5)
        assert(results['df'] == 3)

        results = fisher_freeman_halton(np.array([[5, 0], [0, 5]]))
        self.assertAlmostEqual(results['p'], 0.002, 3)
        self.assertAlmostEqual(results['t'], 9.690985, 5)
        assert(results['df'] == 1)

        results = fisher_freeman_halton(np.array([[2, 4, 2, 4, 6], [3, 1, 3, 5, 7]]))
        self.assertAlmostEqual(results['p'], 0.66, 2)
        self.assertAlmostEqual(results['t'], 2.410306, 5)
        assert(results['df'] == 4)

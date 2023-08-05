import copy
import unittest

from c2s2.base.data import get_simple_samples


class TestSample(unittest.TestCase):

    def setUp(self) -> None:
        self._samples = get_simple_samples()

    def test_copy(self):
        """
        Test shallow copy of `Sample`. The sample must be copied such that phenotypic features maintain value equality
        but are different instances. We need different instances to support perturbation that replace `pf.term_id`
        with ancestor(s).
        """
        copies = [copy.copy(sample) for sample in self._samples]
        for orig, cc in zip(self._samples, copies):
            # We allow to copy the identifier reference since modifying the id moves the backing data.
            self.assertTrue(orig.identifier is cc.identifier)

            # However, phenotypic features must be different instances with value equality
            for orig_pf, cc_pf in zip(orig.phenotypic_features, cc.phenotypic_features):
                self.assertFalse(orig_pf is cc_pf)
                self.assertEqual(orig_pf, cc_pf)


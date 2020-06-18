import unittest
from reckit.random import randint_choice
from reckit.random import batch_randint_choice
import numpy as np


class TestRandintChoice(unittest.TestCase):

    def test_exclusion(self):
        high = 2020

        with self.assertRaises(ValueError):
            randint_choice(high, size=high+1, replace=True, p=None, exclusion=np.arange(high))

        with self.assertRaises(ValueError):
            randint_choice(high, size=high+1, replace=True, p=None, exclusion=np.arange(high+1))

        samples = randint_choice(high, size=high+1, replace=True, p=None, exclusion=None)

        exclusion = np.arange(high-20)
        samples = randint_choice(high, size=high+1, replace=True, p=None, exclusion=exclusion)
        self.assertEqual(len(samples), high+1)
        for s in samples:
            self.assertNotIn(s, exclusion)

        exclusion = set(np.random.choice(high, size=int(high/10), replace=False))
        samples = randint_choice(high, size=high+1, replace=True, p=None, exclusion=exclusion)
        self.assertEqual(len(samples), high+1)
        for s in samples:
            self.assertNotIn(s, exclusion)

    def test_prob(self):
        high = 20
        p = randint_choice(high, size=high, replace=True, p=None, exclusion=None)
        p = np.array(p)/sum(p)
        num_samples = high*20000
        exclusion = []
        samples = randint_choice(high, size=num_samples, replace=True, p=p, exclusion=exclusion)
        frequence = np.zeros_like(p)
        for s in samples:
            frequence[s] += 1
        frequence = frequence/num_samples
        exc_flag = np.zeros_like(p)
        for e in exclusion:
            exc_flag[e] = 1
        compare = np.concatenate([np.expand_dims(p, axis=1),
                                  np.expand_dims(frequence, axis=1),
                                  np.expand_dims(exc_flag, axis=1)], axis=1)
        np_samples = np.random.choice(np.arange(high), size=num_samples, p=p)
        np_frequence = np.zeros_like(p)
        for s in np_samples:
            np_frequence[s] += 1
        np_frequence = np_frequence/num_samples

    def test_replace(self):
        high = 2020

        with self.assertRaises(TypeError):
            randint_choice(high, replace=1)

        with self.assertRaises(ValueError):
            exclusion = set(np.random.choice(high, size=int(high / 10), replace=False))
            randint_choice(high, size=high-10, replace=False, p=None, exclusion=exclusion)

        with self.assertRaises(ValueError):
            randint_choice(high, size=high+1, replace=False, p=None, exclusion=None)

        with self.assertRaises(ValueError):
            randint_choice(high, size=high, replace=False, p=None, exclusion=None)

        samples = randint_choice(high, size=high-1, replace=False, p=None, exclusion=None)
        self.assertEqual(len(samples), len(set(samples)))
        self.assertEqual(len(samples), high-1)

        samples = randint_choice(high, size=high-100, replace=False, p=None, exclusion=None)
        self.assertEqual(len(samples), len(set(samples)))
        self.assertEqual(len(samples), high-100)

        samples = randint_choice(high, size=100, replace=False, p=None, exclusion=None)
        self.assertEqual(len(samples), len(set(samples)))

        exclusion = set(np.random.choice(high, size=int(high/10), replace=False))
        samples = randint_choice(high, size=1000, replace=False, p=None, exclusion=exclusion)
        self.assertEqual(len(samples), len(set(samples)))
        for s in samples:
            self.assertNotIn(s, exclusion)

    def test_size(self):
        high = 2020

        with self.assertRaises(ValueError):
            randint_choice(high, size=0, replace=True, p=None, exclusion=None)

        samples = randint_choice(high, size=1, replace=True, p=None, exclusion=None)
        self.assertIsInstance(samples, int)

        samples = randint_choice(high, size=high+1, replace=True, p=None, exclusion=None)
        self.assertIsInstance(samples, list)


class TestBatchRandintChoice(unittest.TestCase):

    def test_result(self):
        high = 2020
        batch_size = 1000
        size = np.random.choice(np.arange(10, int(high/10)), size=batch_size, replace=True)
        exclusion = [set(np.random.choice(high, size=100+i, replace=False)) for i in range(batch_size)]
        results = batch_randint_choice(high, size=size, replace=True, p=None, exclusion=exclusion)
        self.assertEqual(len(results), batch_size)
        for result, excl in zip(results, exclusion):
            for s in result:
                self.assertNotIn(s, excl)


if __name__ == '__main__':
    unittest.main()

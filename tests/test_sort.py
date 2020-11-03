import unittest
import numpy as np
from reckit import sort, arg_sort, top_k, arg_top_k
import time


class TestSort(unittest.TestCase):
    
    def test_sort_1d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=100000)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.sort(array)
            print(time.time()-start_t)
            start_t = time.time()
            reckit_result = sort(array)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result-reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=100000).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.sort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = sort(array)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

    def test_sort_2d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=(1000, 1000))
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.sort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = sort(array, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=(1000, 1000)).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.sort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = sort(array, n_threads=4)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)
    
    def test_arg_sort_1d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=100000)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_sort(array)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=100000).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_sort(array)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)
    
    def test_arg_sort_2d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=(1000, 1000))
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_sort(array, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=(1000, 1000)).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(array)
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_sort(array, n_threads=4)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)
    
    def test_top_k_1d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=100000)
        k = 100
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = -np.sort(-np.asarray(array))[:k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = top_k(array, k, n_threads=4)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=100000).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = -np.sort(-np.asarray(array))[:k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = top_k(array, k, n_threads=4)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)
    
    def test_top_k_2d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=(1000, 1000))
        k = 100
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = -np.sort(-np.asarray(array))[:, :k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=(1000, 1000)).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = -np.sort(-np.asarray(array))[:, :k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)
    
    def test_arg_top_k_1d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=100000)
        k = 100
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(-np.asarray(array))[:k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=100000).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(-np.asarray(array))[:k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            # self.assertTrue(diff < 0.1)
    
    def test_arg_top_k_2d(self):
        array_ori = np.random.uniform(low=-100.0, high=100.0, size=(1000, 1000))
        k = 100
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(-np.asarray(array))[:, :k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            self.assertTrue(diff < 0.1)

        array_ori = np.random.uniform(low=-100000.0, high=100000.0, size=(1000, 1000)).astype(np.int64)
        for array in [array_ori, array_ori.tolist()]:
            print()
            start_t = time.time()
            np_result = np.argsort(-np.asarray(array))[:, :k]
            print(time.time() - start_t)
            start_t = time.time()
            reckit_result = arg_top_k(array, topk=k, n_threads=2)
            print(time.time() - start_t)
            diff = np.abs(np.sum(np_result - reckit_result))
            print(diff)
            # self.assertTrue(diff < 0.1)


if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from data.sampler import _generate_positive_items
from data.sampler import _sampling_negative_items
from data.sampler import _generative_time_order_positive_items
from data.sampler import PointwiseSampler, PairwiseSampler
from data.sampler import TimeOrderPointwiseSampler, TimeOrderPairwiseSampler
from data.dataset import Dataset


def is_sub_sequence(sequence, sub_seq):
    l1, l2 = len(sequence), len(sub_seq)
    for i in range(l1):
        results = sequence[i:i + l2] == sub_seq
        if sum(results) == l2:
            return True
    return False


class TestFunc(unittest.TestCase):

    def _generate_data(self, num_users, num_items):
        pos_list_dict = {}
        pos_set_dict = {}
        for u in range(num_users):
            size = np.random.choice(np.arange(20, 100))
            items = np.random.choice(num_items, size=size)
            pos_list_dict[u] = items
            pos_set_dict[u] = set(items)
        return pos_list_dict, pos_set_dict

    def test_generate_positive(self):
        with self.assertRaises(TypeError):
            _generate_positive_items(0)

        with self.assertRaises(TypeError):
            _generate_positive_items(None)

        with self.assertRaises(ValueError):
            _generate_positive_items(dict())

        num_users = 100
        num_items = 1000
        pos_list_dict, pos_set_dict = self._generate_data(num_users, num_items)
        user_pos_len, users_list, pos_items_list = _generate_positive_items(pos_list_dict)
        users, pos_lens = list(zip(*user_pos_len))

        self.assertEqual(len(users_list), len(pos_items_list))
        self.assertEqual(sum(pos_lens), len(pos_items_list))
        for user, p_len in user_pos_len:
            self.assertEqual(len(pos_list_dict[user]), p_len)

        pad_len = [0]
        pad_len.extend(pos_lens)
        cum_len_sum = np.cumsum(pad_len)
        for idx, (user, pos_items) in enumerate(pos_list_dict.items()):
            begin, end = cum_len_sum[idx], cum_len_sum[idx+1]
            self.assertEqual(pos_lens[idx], len(pos_items))
            self.assertEqual(end-begin, len(pos_items))
            self.assertEqual(set(pos_items_list[begin:end]), pos_set_dict[user])
            for pos_i in pos_items_list[begin:end]:
                self.assertIn(pos_i, pos_set_dict[user])

    def test_generate_time_positive(self):
        with self.assertRaises(TypeError):
            _generative_time_order_positive_items(0)

        with self.assertRaises(TypeError):
            _generative_time_order_positive_items(None)

        with self.assertRaises(ValueError):
            _generative_time_order_positive_items(dict())

        num_users = 100
        num_items = 1000
        pos_list_dict, pos_set_dict = self._generate_data(num_users, num_items)

        with self.assertRaises(ValueError):
            _generative_time_order_positive_items(pos_list_dict, 0)

        with self.assertRaises(ValueError):
            _generative_time_order_positive_items(pos_list_dict, -1)

        for high_order in (1, 2, 10, 50, 101):
            print(high_order)
            user_pos_len, users_list, recent_items_list, pos_items_list =\
                _generative_time_order_positive_items(pos_list_dict, high_order)
            self.assertEqual(len(users_list), len(pos_items_list))
            self.assertEqual(len(recent_items_list), len(pos_items_list))
            if not pos_items_list:
                continue
            users, pos_lens = list(zip(*user_pos_len))
            self.assertEqual(sum(pos_lens), len(pos_items_list))
            self.assertEqual(len(pos_lens), sum([len(items)>high_order for u, items in pos_list_dict.items()]))

            pad_len = [0]
            pad_len.extend(pos_lens)
            cum_len_sum = np.cumsum(pad_len)

            for idx, (user, p_len) in enumerate(user_pos_len):
                self.assertEqual(len(pos_list_dict[user])-high_order, p_len)
                begin, end = cum_len_sum[idx], cum_len_sum[idx + 1]
                self.assertEqual(end - begin, p_len)
                for i in range(begin, end):
                    user, r_items, pos_item = users_list[i], recent_items_list[i], pos_items_list[i]
                    if high_order == 1:
                        r_items = [r_items]
                    else:
                        r_items = list(r_items)
                    self.assertTrue(is_sub_sequence(pos_list_dict[user], r_items))
                    r_items.append(pos_item)
                    self.assertTrue(is_sub_sequence(pos_list_dict[user], r_items))

    def test_sampling_negative(self):
        num_users = 100
        num_items = 1000
        pos_list_dict, pos_set_dict = self._generate_data(num_users, num_items)
        user_pos_len, users_list, pos_items_list = _generate_positive_items(pos_list_dict)
        users, pos_lens = list(zip(*user_pos_len))

        with self.assertRaises(ValueError):
            _sampling_negative_items(user_pos_len, 0, num_items, pos_list_dict)

        with self.assertRaises(ValueError):
            _sampling_negative_items(user_pos_len, -1, num_items, pos_list_dict)

        for neg_num in (1, 2, 4, 400):
            neg_items_list = _sampling_negative_items(user_pos_len, neg_num, num_items, pos_list_dict)
            self.assertEqual(sum(pos_lens), len(neg_items_list))
            self.assertEqual(len(users_list), len(neg_items_list))
            for neg_items in neg_items_list:
                if neg_num == 1:
                    self.assertIsInstance(neg_items, int)
                else:
                    self.assertEqual(len(neg_items), neg_num)

            for user, neg_items in zip(users_list, neg_items_list):
                if neg_num == 1:
                    self.assertNotIn(neg_items, pos_set_dict[user])
                else:
                    for neg_j in neg_items:
                        self.assertNotIn(neg_j, pos_set_dict[user])


class TestPointwise(unittest.TestCase):

    def setUp(self):
        train_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.train"
        test_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.test"
        format = "UIRT"
        sep = ","
        self.dataset = Dataset(train_file, test_file, format, sep)
        user_pos_dict = self.dataset.get_user_train_dict()
        user_pos_dict = {user: set(items) for user, items in user_pos_dict.items()}
        self.user_pos_dict = user_pos_dict

    def test_neg_num(self):
        for neg_num in (1, 2, 10):
            print(neg_num)
            sampler = PointwiseSampler(self.dataset, neg_num=neg_num, shuffle=True, drop_last=False)
            for bat_users, bat_items, bat_labels in sampler:
                for user, item, label in zip(bat_users, bat_items, bat_labels):
                    if label == 0:
                        self.assertNotIn(item, self.user_pos_dict[user])
                    else:
                        self.assertIn(item, self.user_pos_dict[user])

    def test_batch_size(self):
        for bat_size in (1, 2, 1024):
            print(bat_size)
            sampler = PointwiseSampler(self.dataset, neg_num=2, batch_size=bat_size, shuffle=True, drop_last=False)
            for bat_users, bat_items, bat_labels in sampler:
                for user, item, label in zip(bat_users, bat_items, bat_labels):
                    if label == 0:
                        self.assertNotIn(item, self.user_pos_dict[user])
                    else:
                        self.assertIn(item, self.user_pos_dict[user])


class TestPairwise(unittest.TestCase):

    def setUp(self):
        train_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.train"
        test_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.test"
        format = "UIRT"
        sep = ","
        self.dataset = Dataset(train_file, test_file, format, sep)
        user_pos_dict = self.dataset.get_user_train_dict()
        user_pos_dict = {user: set(items) for user, items in user_pos_dict.items()}
        self.user_pos_dict = user_pos_dict

    def test_neg_num(self):
        for neg_num in (1, 2, 10):
            print(neg_num)
            sampler = PairwiseSampler(self.dataset, neg_num=neg_num, shuffle=True, drop_last=False)
            for bat_users, bat_pos_items, bat_neg_items in sampler:
                for user, pos_item, neg_item in zip(bat_users, bat_pos_items, bat_neg_items):
                    if neg_num == 1:
                        self.assertNotIn(neg_item, self.user_pos_dict[user])
                    else:
                        for neg_j in neg_item:
                            self.assertNotIn(neg_j, self.user_pos_dict[user])
                    self.assertIn(pos_item, self.user_pos_dict[user])

    def test_batch_size(self):
        for bat_size in (1, 2, 1024):
            print(bat_size)
            sampler = PairwiseSampler(self.dataset, neg_num=2, batch_size=bat_size, shuffle=True, drop_last=False)
            for bat_users, bat_pos_items, bat_neg_items in sampler:
                for user, pos_item, neg_item in zip(bat_users, bat_pos_items, bat_neg_items):
                    for neg_j in neg_item:
                        self.assertNotIn(neg_j, self.user_pos_dict[user])
                    self.assertIn(pos_item, self.user_pos_dict[user])


class TestTimePointwise(unittest.TestCase):

    def setUp(self):
        train_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.train"
        test_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.test"
        format = "UIRT"
        sep = ","
        self.dataset = Dataset(train_file, test_file, format, sep)
        user_pos_dict = self.dataset.get_user_train_dict(by_time=True)
        self.user_pos_list_dict = user_pos_dict
        user_pos_dict = {user: set(items) for user, items in user_pos_dict.items()}
        self.user_pos_set_dict = user_pos_dict

    def test_neg_num(self):
        for neg_num in (1, 2, 10):
            print(neg_num)
            sampler = TimeOrderPointwiseSampler(self.dataset, high_order=1, neg_num=neg_num,
                                                shuffle=True, drop_last=False)
            for bat_users, bat_recent_items, bat_next_items, bat_labels in sampler:
                for user, recent_items, next_item, label in zip(bat_users, bat_recent_items, bat_next_items, bat_labels):
                    if label == 0:
                        self.assertNotIn(next_item, self.user_pos_set_dict[user])
                    else:
                        self.assertIn(next_item, self.user_pos_set_dict[user])
                        self.assertTrue(is_sub_sequence(self.user_pos_list_dict[user], [recent_items, next_item]))

    def test_high_order(self):
        for high_order in (2, 1, 10):
            print(high_order)
            sampler = TimeOrderPointwiseSampler(self.dataset, high_order=high_order, neg_num=2,
                                                shuffle=False, drop_last=False)
            for bat_users, bat_recent_items, bat_next_items, bat_labels in sampler:
                for user, recent_items, next_item, label in zip(bat_users, bat_recent_items, bat_next_items, bat_labels):
                    if label == 0:
                        self.assertNotIn(next_item, self.user_pos_set_dict[user])
                    else:
                        self.assertIn(next_item, self.user_pos_set_dict[user])
                        if high_order == 1:
                            recent_items = [recent_items]

                        sequence = self.user_pos_list_dict[user]
                        sub_seq = list(recent_items) + [next_item]
                        self.assertTrue(is_sub_sequence(sequence, sub_seq))

    def test_batch_size(self):
        for bat_size in (1, 2, 1024):
            print(bat_size)
            sampler = TimeOrderPointwiseSampler(self.dataset, high_order=2, neg_num=2,
                                                batch_size=bat_size, shuffle=False, drop_last=False)
            for bat_users, bat_recent_items, bat_next_items, bat_labels in sampler:
                for user, recent_items, next_item, label in zip(bat_users, bat_recent_items, bat_next_items,
                                                                bat_labels):
                    if label == 0:
                        self.assertNotIn(next_item, self.user_pos_set_dict[user])
                    else:
                        self.assertIn(next_item, self.user_pos_set_dict[user])

                        sequence = self.user_pos_list_dict[user]
                        sub_seq = list(recent_items) + [next_item]
                        self.assertTrue(is_sub_sequence(sequence, sub_seq))


class TestTimePairwise(unittest.TestCase):

    def setUp(self):
        train_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.train"
        test_file = "../dataset/Video_Games/Video_Games_loo_u5_i5.test"
        format = "UIRT"
        sep = ","
        self.dataset = Dataset(train_file, test_file, format, sep)
        user_pos_dict = self.dataset.get_user_train_dict(by_time=True)
        self.user_pos_list_dict = user_pos_dict
        user_pos_dict = {user: set(items) for user, items in user_pos_dict.items()}
        self.user_pos_set_dict = user_pos_dict

    def test_neg_num(self):
        for neg_num in (1, 2, 10):
            print(neg_num)
            sampler = TimeOrderPairwiseSampler(self.dataset, high_order=1, neg_num=neg_num,
                                               shuffle=True, drop_last=False)
            for bat_users, bat_recent_items, bat_pos_items, bat_neg_items in sampler:
                for user, recent_items, pos_item, neg_item in zip(bat_users, bat_recent_items, bat_pos_items, bat_neg_items):
                    if neg_num == 1:
                        self.assertNotIn(neg_item, self.user_pos_set_dict[user])
                    else:
                        for neg_j in neg_item:
                            self.assertNotIn(neg_j, self.user_pos_set_dict[user])
                    self.assertIn(pos_item, self.user_pos_set_dict[user])
                    self.assertTrue(is_sub_sequence(self.user_pos_list_dict[user], [recent_items, pos_item]))

    def test_high_order(self):
        for high_order in (2, 1, 10):
            print(high_order)
            sampler = TimeOrderPairwiseSampler(self.dataset, high_order=high_order, neg_num=2,
                                               shuffle=False, drop_last=False)

            for bat_users, bat_recent_items, bat_pos_items, bat_neg_items in sampler:
                for user, recent_items, pos_item, neg_item in zip(bat_users, bat_recent_items, bat_pos_items, bat_neg_items):
                    for neg_j in neg_item:
                        self.assertNotIn(neg_j, self.user_pos_set_dict[user])
                    self.assertIn(pos_item, self.user_pos_set_dict[user])

                    if high_order == 1:
                        recent_items = [recent_items]

                    sequence = self.user_pos_list_dict[user]
                    sub_seq = list(recent_items) + [pos_item]
                    self.assertTrue(is_sub_sequence(sequence, sub_seq))

    def test_batch_size(self):
        for bat_size in (1, 2, 1024):
            print(bat_size)
            sampler = TimeOrderPairwiseSampler(self.dataset, high_order=2, neg_num=2,
                                               batch_size=bat_size, shuffle=False, drop_last=False)
            for bat_users, bat_recent_items, bat_pos_items, bat_neg_items in sampler:
                for user, recent_items, pos_item, neg_item in zip(bat_users, bat_recent_items, bat_pos_items, bat_neg_items):
                    for neg_j in neg_item:
                        self.assertNotIn(neg_j, self.user_pos_set_dict[user])
                    self.assertIn(pos_item, self.user_pos_set_dict[user])

                    sequence = self.user_pos_list_dict[user]
                    sub_seq = list(recent_items) + [pos_item]
                    self.assertTrue(is_sub_sequence(sequence, sub_seq))


if __name__ == '__main__':
    unittest.main()

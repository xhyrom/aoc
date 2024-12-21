import unittest

from priority_queue import priority_queue


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = priority_queue([5, 1, 3])

    def test_initial_elements(self):
        self.assertEqual(len(self.pq), 3)
        self.assertEqual(list(self.pq), [1, 3, 5])

    def test_append(self):
        self.pq.append(2)
        self.assertEqual(len(self.pq), 4)
        self.assertEqual(list(self.pq), [1, 2, 3, 5])

    def test_appendleft(self):
        self.pq.appendleft(4)
        self.assertEqual(len(self.pq), 4)
        self.assertEqual(list(self.pq), [1, 3, 4, 5])

    def test_pop(self):
        self.assertEqual(self.pq.pop(), 1)
        self.assertEqual(len(self.pq), 2)
        self.assertEqual(list(self.pq), [3, 5])

    def test_popleft(self):
        self.assertEqual(self.pq.popleft(), 1)
        self.assertEqual(len(self.pq), 2)
        self.assertEqual(list(self.pq), [3, 5])

    def test_pop_empty(self):
        empty_pq = priority_queue()
        with self.assertRaises(IndexError):
            empty_pq.pop()

    def test_popleft_empty(self):
        empty_pq = priority_queue()
        with self.assertRaises(IndexError):
            empty_pq.popleft()

    def test_len(self):
        self.assertEqual(len(self.pq), 3)
        self.pq.append(6)
        self.assertEqual(len(self.pq), 4)

    def test_iter(self):
        self.assertEqual(list(iter(self.pq)), [1, 3, 5])

    def test_repr(self):
        self.assertEqual(repr(self.pq), "priority_queue([1, 3, 5])")


if __name__ == "__main__":
    unittest.main()

#!/bin/env python3

import unittest

import hypothesis
import hypothesis.strategies as st

import shuffle


class TestFisherYatesShuffle(unittest.TestCase):

    @hypothesis.given(st.lists(st.integers(), unique=True))
    @hypothesis.example([])
    def test_simple(self, integers):
        shuffled = shuffle.fisher_yates_shuffle(integers)
        self.assertEqual(len(integers), len(shuffled))


if __name__ == '__main__':
    unittest.main()

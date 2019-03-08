#!/bin/env python3

import unittest

import hypothesis
import hypothesis.strategies as st

import shuffle


class TestFisherYatesShuffle(unittest.TestCase):

    @hypothesis.given(st.lists(st.integers(), unique=True))
    @hypothesis.example([])
    def test_property_length(self, integers):
        """Test simple properties of the function.

        - Length does not change after shuffling
        - Content doesn't change after shuffling
        """
        shuffled = shuffle.fisher_yates_shuffle(integers)
        self.assertEqual(len(integers), len(shuffled))
        self.assertEqual(set(integers), set(shuffled))

    @hypothesis.given(st.lists(st.integers(), unique=True, min_size=20))
    def test_property_order(self, integers):
        """Test more properties of the function.

        - With larger lists, we expect that the order changes
          after a shuffle
        """
        shuffled = shuffle.fisher_yates_shuffle(integers)
        self.assertEqual(set(integers), set(shuffled))
        self.assertNotEqual(integers, shuffled)



if __name__ == '__main__':
    unittest.main()

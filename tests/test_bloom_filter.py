import unittest
from random import shuffle

from python.bloomfilter.bloom import BloomFilter


class TestBloomFilter(unittest.TestCase):
    def test_basic(self):
        n = 20  # no of items to add
        p = 0.05  # false positive probability
        bloomf = BloomFilter(n, p)

        # print("Size of bit array:{}".format(bloomf.size))
        # print("Number of hash functions:{}".format(bloomf.hash_count))
        # Good property to test:
        # print("False positive Probability:{}".format(bloomf.fp_prob))

        # words to be added
        word_present = [
            "abound",
            "abounds",
            "abundance",
            "abundant",
            "accessable",
            "bloom",
            "blossom",
            "bolster",
            "bonny",
            "bonus",
            "bonuses",
            "coherent",
            "cohesive",
            "colorful",
            "comely",
            "comfort",
            "gems",
            "generosity",
            "generous",
            "generously",
            "genial",
        ]

        for item in word_present:
            bloomf.add(item)

        # word not added
        word_absent = [
            "bluff",
            "cheater",
            "hate",
            "war",
            "humanity",
            "racism",
            "hurt",
            "nuke",
            "gloomy",
            "facebook",
            "geeksforgeeks",
            # "twitter",
        ]

        shuffle(word_present)
        shuffle(word_absent)
        test_words = word_present[:10] + word_absent
        shuffle(test_words)

        for word in test_words:
            if word in word_absent:
                self.assertFalse(bloomf.check(word), msg=word)

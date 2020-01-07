#!/bin/env python3

import itertools
import unittest

import hypothesis
import hypothesis.strategies as st

from python.btclient.btorrent import tokenize


def bencode_integer(integer):
    return f"i{integer}e"


def bencode_bytes(text):
    return f"{len(text)}:{text}"


class TestBTorrentTokenizer(unittest.TestCase):
    """Test suite for the BTorrent stream tokenizer.

    Spec: [Wikipedia](https://en.wikipedia.org/wiki/Bencode)
    """

    @hypothesis.given(st.integers())
    def test_tokenize_integer(self, integers):
        """
        > An integer is encoded as i<integer encoded in base ten ASCII>e.
        > Leading zeros are not allowed (although the number zero is still represented as "0").
        > Negative values are encoded by prefixing the number with a hyphen-minus.
        > The number 42 would thus be encoded as i42e, 0 as i0e, and -42 as i-42e.
        > Negative zero is not permitted.
        """
        self.assertEqual(list(tokenize(f"i{integers}e")), ["i", f"{integers}", "e"])

    @hypothesis.given(st.text())
    def test_tokenize_byte_stream(self, text):
        """
        > A byte string (a sequence of bytes, not necessarily characters) is encoded as
        > <length>:<contents>.
        > The length is encoded in base 10, like integers, but must be non-negative (zero is allowed);
        > the contents are just the bytes that make up the string.
        > The string "spam" would be encoded as 4:spam. [...]
        """
        self.assertEqual(list(tokenize(f"{len(text)}:{text}")), ["s", f"{text}"])

    @hypothesis.given(st.data())
    def test_tokenize_list(self, data):
        """TODO: strategy to generate nested lists
        > A list of values is encoded as l<contents>e .
        > The contents consist of the bencoded elements of the list, in order, concatenated.
        > A list consisting of the string "spam" and the number 42 would be encoded as: l4:spami42ee.
        > Note the absence of separators between elements,
        > and the first character is the letter 'l', not digit '1'.

        Test that tokenize(list) == [tokenize(elem) for elem in list].
        Test that list1 != list2 implies tokenize(list1) != tokenize(list2)
        """
        strategy = st.lists(
            st.one_of(
                st.builds(bencode_integer, st.integers()),
                st.builds(bencode_bytes, st.text(min_size=1)),
            ),
            min_size=1,
        )

        x = data.draw(strategy)
        y = data.draw(strategy)
        hypothesis.assume(x != y)

        expected_content = lambda l: itertools.chain.from_iterable(
            tokenize(item) for item in l
        )

        self.assertEqual(
            list(tokenize(f"l{''.join(x)}e")), ["l", *expected_content(x), "e"]
        )
        self.assertNotEqual(
            list(tokenize(f"l{''.join(x)}e")), list(tokenize(f"l{''.join(y)}e"))
        )

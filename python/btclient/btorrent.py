"""Read a btorrent file.

A Simple BitTorrent "bencode" Decoder:
https://effbot.org/zone/bencode.htm
"""

import re

START_END_REGEX = re.compile("(?P<mark>[idel])|(?P<str>\d+):|(?P<int>-?\d+)")


def tokenize(file_bytes):
    """Tokenize a btorrent stream.

    >>> list(tokenize("4:spam"))
    ['s', 'spam']
    >>> list(tokenize("i3e")) # int
    ['i', '3', 'e']
    >>> list(tokenize("i-3e"))
    ['i', '-3', 'e']
    >>> list(tokenize("l4:spam4:eggse")) # list
    ['l', 's', 'spam', 's', 'eggs', 'e']
    >>> list(tokenize("li0ee"))
    ['l', 'i', '0', 'e', 'e']
    >>> list(tokenize("d3:cow3:moo4:spam4:eggse")) # dict
    ['d', 's', 'cow', 's', 'moo', 's', 'spam', 's', 'eggs', 'e']
    """
    i = 0
    file_length = len(file_bytes)
    while i < file_length:
        match = START_END_REGEX.match(file_bytes, i)
        # match_len = match.group(match.lastindex)
        i = match.end()
        if match.group("str"):
            yield "s"
            str_len = int(match.group("str"))
            yield file_bytes[i : i + str_len]
            i += str_len
        elif match.group("mark"):
            yield match.group("mark")
        elif match.group("int"):
            yield match.group("int")


def decode_item(get_next, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(get_next())
        if get_next() != "e":
            raise ValueError
    elif token == "s":
        # string: "s" value (virtual tokens)
        data = get_next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = get_next()
        while tok != "e":
            data.append(decode_item(get_next, tok))
            tok = get_next()
        if token == "d":
            data = dict(zip(data[0::2], data[1::2]))
    else:
        raise ValueError
    return data


def decode(file_bytes):
    try:
        src = tokenize(file_bytes)
        data = decode_item(src.__next__, next(src))
        for token in src:  # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()

"""Read a btorrent file.

A Simple BitTorrent "bencode" Decoder:
https://effbot.org/zone/bencode.htm
"""

import re

START_END_REGEX = re.compile("([idel])|(\d+):|(-?\d+)")


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
        m = START_END_REGEX.match(file_bytes, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield file_bytes[i : i + int(s)]
            i += int(s)
        else:
            yield s


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

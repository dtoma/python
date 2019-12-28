import random
from typing import List, TypeVar

T = TypeVar("T")


def fisher_yates_shuffle(items: List[T]) -> List[T]:
    """Return a shuffled list of elements.

    Source:
    https://spin.atomicobject.com/2014/08/11/fisher-yates-shuffle-randomization-algorithm/
    """
    items = items.copy()
    nb_items = len(items)
    for i in range(nb_items):
        random_index = random.randint(i, nb_items - 1)
        items[i], items[random_index] = items[random_index], items[i]
    return items

REQUIRED_VALUES = frozenset(range(1, 17))


def satisfies_set_equality(grid):
    return set(grid) == REQUIRED_VALUES

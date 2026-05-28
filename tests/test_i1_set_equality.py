from magic_square.invariants import satisfies_set_equality


def test_full_valid_set_1_to_16_satisfies_i1():
    grid = list(range(1, 17))
    assert satisfies_set_equality(grid) is True

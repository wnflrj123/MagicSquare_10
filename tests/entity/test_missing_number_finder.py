"""D-MISS-* — MissingNumberFinder 도메인 단위 테스트.

보호 invariant: I8 (작은 수 먼저 정렬)
FR: FR-03 (PRD §6 FR-03)
"""
from entity.missing_number_finder import MissingNumberFinder
from entity.value_objects import MissingPair


def test_missing_finder_returns_sorted_pair_d_miss_01():
    """D-MISS-01 — 누락된 두 수를 (작은 수, 큰 수) 순서로 반환."""
    # Arrange — Dürer 마방진에서 7, 12 가린 격자
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 0, 0],
        [4, 15, 14, 1],
    ]

    # Act
    pair = MissingNumberFinder.find(grid)

    # Assert
    assert pair == MissingPair(n_small=7, n_big=12)


def test_missing_finder_adjacent_small_numbers_d_miss_02():
    """D-MISS-02 — 누락 수가 1·2처럼 인접해도 정렬 반환."""
    # Arrange — 1과 2가 빠진 격자
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]

    # Act
    pair = MissingNumberFinder.find(grid)

    # Assert
    assert pair == MissingPair(n_small=1, n_big=2)


def test_missing_finder_extreme_numbers_d_miss_03():
    """D-MISS-03 — 1과 16처럼 양 끝 수가 누락되어도 정렬 반환."""
    # Arrange
    grid = [
        [0, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]

    # Act
    pair = MissingNumberFinder.find(grid)

    # Assert
    assert pair == MissingPair(n_small=1, n_big=16)

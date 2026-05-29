"""D-LOC-* — BlankFinder 도메인 단위 테스트.

보호 invariant: I7 (빈칸 순서 = row-major 스캔 순서)
FR: FR-02 (PRD §6 FR-02)
"""
from entity.blank_finder import BlankFinder
from entity.value_objects import Coordinate


def test_blank_finder_returns_two_coords_in_row_major_order_d_loc_01():
    """D-LOC-01 — 정상 빈칸 2개를 row-major 순서로 반환."""
    # Arrange
    grid = [
        [0, 1, 2, 3],
        [4, 5, 0, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15],
    ]

    # Act
    coords = BlankFinder.find(grid)

    # Assert
    assert coords == [Coordinate(1, 1), Coordinate(2, 3)]


def test_blank_finder_handles_blanks_at_last_row_d_loc_02():
    """D-LOC-02 — 빈칸이 끝줄·끝열에 있을 때도 정상."""
    # Arrange
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 0],
    ]

    # Act
    coords = BlankFinder.find(grid)

    # Assert
    assert coords == [Coordinate(4, 3), Coordinate(4, 4)]


def test_blank_finder_handles_blanks_far_apart_d_loc_03():
    """D-LOC-03 — 빈칸이 첫 칸과 마지막 칸에 떨어져 있어도 row-major 유지."""
    # Arrange
    grid = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 0],
    ]

    # Act
    coords = BlankFinder.find(grid)

    # Assert
    assert coords == [Coordinate(1, 1), Coordinate(4, 4)]

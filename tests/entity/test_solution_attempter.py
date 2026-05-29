"""D-ATT-* — SolutionAttempter 도메인 단위 테스트.

보호: 순수 함수성 (입력 불변 + 결정성)
FR: FR-05 (PRD §6 FR-05)
"""
from entity.solution_attempter import SolutionAttempter
from entity.value_objects import Coordinate


def test_attempter_places_pair_at_blank_coords_d_att_01():
    """D-ATT-01 — 두 빈칸에 (n_a, n_b)를 정확히 배치한 새 격자 반환, 입력은 불변."""
    # Arrange
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [0, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    blanks = [Coordinate(1, 3), Coordinate(3, 1)]
    pair = (2, 9)

    # Act
    result_grid = SolutionAttempter.apply(grid, blanks, pair)

    # Assert
    assert result_grid[0][2] == 2  # (1,3) — 1-index → [0][2]
    assert result_grid[2][0] == 9  # (3,1) → [2][0]
    # 입력 불변
    assert grid[0][2] == 0
    assert grid[2][0] == 0


def test_attempter_is_deterministic_d_att_02():
    """D-ATT-02 — 동일 입력에 두 번 호출하면 동일 출력 (순수 함수)."""
    # Arrange
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [0, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    blanks = [Coordinate(1, 3), Coordinate(3, 1)]
    pair = (2, 9)

    # Act
    r1 = SolutionAttempter.apply(grid, blanks, pair)
    r2 = SolutionAttempter.apply(grid, blanks, pair)

    # Assert
    assert r1 == r2

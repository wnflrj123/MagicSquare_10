"""I-INT-* — Boundary → Control → Domain 통합 테스트.

보호 invariant: 전체 (I1~I12) — Boundary 검증 + Domain 풀이 + 결과 변환
FR: FR-01 + FR-06 + FR-07 + FR-08 (PRD §6)
"""
from boundary.solve_boundary import SolveBoundary
from boundary.error_codes import ErrorCode
from control.solve_partial_magic_square import SolvePartialMagicSquare


def _make_boundary() -> SolveBoundary:
    """Composition root — boundary가 control을 통해 domain을 호출."""
    return SolveBoundary(use_case=SolvePartialMagicSquare())


def test_valid_step_a_end_to_end_i_int_01(partial_step_a_grid):
    """I-INT-01 — 유효 입력 + Step A 성공 (end-to-end)."""
    # Act
    result = _make_boundary().solve(partial_step_a_grid)

    # Assert
    assert result.is_ok is True
    assert result.value == [1, 3, 2, 3, 1, 9]


def test_valid_step_b_reverse_end_to_end_i_int_02(partial_step_b_grid):
    """I-INT-02 — 유효 입력 + Step A 실패·Step B 성공 (end-to-end)."""
    # Act
    result = _make_boundary().solve(partial_step_b_grid)

    # Assert
    assert result.is_ok is True
    assert result.value == [1, 1, 16, 4, 4, 1]


def test_invalid_size_blocks_domain_i_int_03():
    """I-INT-03 — 4x4 아닌 입력 → E001, Domain 호출 0회."""
    # Arrange — Boundary는 invalid 입력에 대해 Domain 호출 차단
    boundary = _make_boundary()

    # Act
    result = boundary.solve([[1, 2, 3]])

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE


def test_invalid_blank_count_blocks_domain_i_int_04(durer_grid):
    """I-INT-04 — 빈칸≠2 → E002, Domain 호출 0회."""
    # Arrange
    boundary = _make_boundary()

    # Act
    result = boundary.solve(durer_grid)  # 빈칸 0개

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_BLANK_COUNT


def test_invalid_value_range_blocks_domain_i_int_05():
    """I-INT-05 — 값 범위 위반 → E003."""
    # Arrange
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 17],
        [4, 15, 14, 0],
    ]
    boundary = _make_boundary()

    # Act
    result = boundary.solve(grid)

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_VALUE_RANGE


def test_duplicate_value_blocks_domain_i_int_06():
    """I-INT-06 — 0 제외 중복 → E004."""
    # Arrange
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 5, 12],  # 5 중복
        [4, 15, 14, 0],
    ]
    boundary = _make_boundary()

    # Act
    result = boundary.solve(grid)

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.DUPLICATE_VALUE


def test_unsolvable_returns_e005_i_int_07(unsolvable_grid):
    """I-INT-07 — 유효 입력이지만 Step A·B 모두 실패 → E005."""
    # Act
    result = _make_boundary().solve(unsolvable_grid)

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.NO_VALID_MAGIC_SQUARE
    assert result.error.message == "No valid magic square found."

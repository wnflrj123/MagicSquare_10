"""C-SOL-* — SolvePartialMagicSquare Use Case 단위 테스트.

보호: Domain 서비스 오케스트레이션 (Boundary 검증된 입력만 받는다고 가정).
FR: FR-07 (PRD §6 FR-07)
"""
from control.solve_partial_magic_square import SolvePartialMagicSquare


def test_use_case_returns_int6_for_valid_partial_step_a_c_sol_01(
    partial_step_a_grid,
):
    """C-SOL-01 — 검증된 부분 마방진 + Step A 성공 → int[6] 반환."""
    # Arrange
    use_case = SolvePartialMagicSquare()

    # Act
    result = use_case.resolve(partial_step_a_grid)

    # Assert
    assert result == [1, 3, 2, 3, 1, 9]


def test_use_case_returns_reverse_for_step_b_c_sol_02(partial_step_b_grid):
    """C-SOL-02 — Step A 실패·Step B 성공 → int[6] (reverse 순서)."""
    # Arrange
    use_case = SolvePartialMagicSquare()

    # Act
    result = use_case.resolve(partial_step_b_grid)

    # Assert
    assert result == [1, 1, 16, 4, 4, 1]

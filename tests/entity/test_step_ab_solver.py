"""D-SOL-* — StepABSolver 도메인 오케스트레이션 테스트.

보호 invariant: I8 (Step A 우선) + I9 (Step B reverse) + I10 (int[6], 1-index)
              + I11 (둘 다 실패 → NoValidMagicSquareError) + I7 (row-major)
FR: FR-06 (PRD §6 FR-06)
"""
import pytest

from entity.step_ab_solver import StepABSolver
from entity.errors import NoValidMagicSquareError


def test_step_a_success_returns_small_first_d_sol_01(partial_step_a_grid):
    """D-SOL-01 — Step A 성공 시 (작은 수→첫 빈칸, 큰 수→둘째)."""
    # Act
    result = StepABSolver.solve(partial_step_a_grid)

    # Assert
    # PARTIAL_STEP_A_GRID: 빈칸 (1,3)·(3,1), 누락 {2,9}, Step A 성공 = [1,3,2,3,1,9]
    assert result == [1, 3, 2, 3, 1, 9]


def test_step_a_fails_step_b_success_returns_big_first_d_sol_02(partial_step_b_grid):
    """D-SOL-02 — Step A 실패·Step B(reverse) 성공 시 (큰 수→첫 빈칸)."""
    # Act
    result = StepABSolver.solve(partial_step_b_grid)

    # Assert
    # PARTIAL_STEP_B_GRID: 빈칸 (1,1)·(4,4), 누락 {1,16}, Step B 성공 = [1,1,16,4,4,1]
    assert result == [1, 1, 16, 4, 4, 1]


def test_both_steps_fail_raises_no_valid_magic_square_d_sol_03(unsolvable_grid):
    """D-SOL-03 — Step A·B 모두 실패 시 NoValidMagicSquareError 발생."""
    # Act / Assert
    with pytest.raises(NoValidMagicSquareError):
        StepABSolver.solve(unsolvable_grid)


def test_solve_output_uses_1_index_coords_d_sol_04(partial_step_a_grid):
    """D-SOL-04 — 출력 좌표 r,c ∈ [1, 4] (1-index 강제)."""
    # Act
    result = StepABSolver.solve(partial_step_a_grid)

    # Assert
    r1, c1, _, r2, c2, _ = result
    assert 1 <= r1 <= 4 and 1 <= c1 <= 4
    assert 1 <= r2 <= 4 and 1 <= c2 <= 4


def test_solve_output_length_is_6_d_sol_05(partial_step_a_grid):
    """D-SOL-05 — 모든 성공 출력 길이는 정확히 6."""
    # Act
    result = StepABSolver.solve(partial_step_a_grid)

    # Assert
    assert len(result) == 6


def test_solve_output_blanks_in_row_major_d_sol_06(partial_step_a_grid):
    """D-SOL-06 — 출력의 첫 좌표(r1,c1)가 row-major상 둘째(r2,c2)보다 앞."""
    # Act
    result = StepABSolver.solve(partial_step_a_grid)

    # Assert
    r1, c1, _, r2, c2, _ = result
    # row-major: r1 < r2, 또는 r1==r2 and c1 < c2
    assert (r1 < r2) or (r1 == r2 and c1 < c2)

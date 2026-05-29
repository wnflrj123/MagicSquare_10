"""U-OUT-* — SolveBoundary 출력 계약 테스트.

보호 invariant: I10 (int[6], 1-index) + I11 (E005 변환) + I12 (Domain mock 가능)
FR: FR-08 (PRD §6 FR-08)
"""
from unittest.mock import MagicMock

from boundary.solve_boundary import SolveBoundary
from boundary.error_codes import ErrorCode
from entity.errors import NoValidMagicSquareError


def test_success_returns_int6_unchanged_u_out_01(partial_step_a_grid):
    """U-OUT-01 — Domain mock이 int[6] 반환 시 Boundary는 변형 없이 그대로 반환."""
    # Arrange
    domain_mock = MagicMock()
    domain_mock.solve.return_value = [1, 1, 7, 2, 3, 12]
    boundary = SolveBoundary(use_case=domain_mock)

    # Act
    result = boundary.solve(partial_step_a_grid)

    # Assert
    assert result.is_ok is True
    assert result.value == [1, 1, 7, 2, 3, 12]
    assert len(result.value) == 6


def test_domain_failure_returns_e005_error_u_out_02(partial_step_a_grid):
    """U-OUT-02 — Domain이 NoValidMagicSquareError 발생 시 Boundary는 E005로 변환."""
    # Arrange
    domain_mock = MagicMock()
    domain_mock.solve.side_effect = NoValidMagicSquareError("...")
    boundary = SolveBoundary(use_case=domain_mock)

    # Act
    result = boundary.solve(partial_step_a_grid)

    # Assert
    assert result.is_error is True
    assert result.error.code == ErrorCode.NO_VALID_MAGIC_SQUARE
    assert result.error.message == "No valid magic square found."


def test_success_output_uses_1_index_u_out_03(partial_step_a_grid):
    """U-OUT-03 — 출력 좌표 r,c ∈ [1,4] (1-index 강제, Domain mock 통과)."""
    # Arrange — Domain mock이 1-index 좌표를 반환한다고 가정
    domain_mock = MagicMock()
    domain_mock.solve.return_value = [1, 3, 2, 3, 1, 9]
    boundary = SolveBoundary(use_case=domain_mock)

    # Act
    result = boundary.solve(partial_step_a_grid)

    # Assert
    r1, c1, _, r2, c2, _ = result.value
    assert 1 <= r1 <= 4 and 1 <= c1 <= 4
    assert 1 <= r2 <= 4 and 1 <= c2 <= 4

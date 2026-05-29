"""U-VAL-* + U-FLOW-* — InputValidator 단위 테스트 (Boundary).

보호 invariant: I1·I2·I3·I4 + I12 (invalid 입력 시 Domain 호출 0회)
FR: FR-01 (PRD §6 FR-01)
"""
from unittest.mock import MagicMock

import pytest

from boundary.input_validator import InputValidator
from boundary.error_codes import ErrorCode


# ---------------------------------------------------------------------------
# U-VAL-01~05 — I1 4x4 검증 (E001 INVALID_SIZE)
# ---------------------------------------------------------------------------
def test_validator_rejects_none_u_val_01():
    """U-VAL-01 — grid=None → E001 INVALID_SIZE."""
    result = InputValidator.validate(None)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE
    assert result.error.message == "Grid must be 4x4."


def test_validator_rejects_3x4_u_val_02():
    """U-VAL-02 — 3x4 행렬 → E001."""
    grid = [[1, 2, 3, 4]] * 3
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE


def test_validator_rejects_4x3_u_val_03():
    """U-VAL-03 — 4x3 행렬 → E001."""
    grid = [[1, 2, 3]] * 4
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE


def test_validator_rejects_5x5_u_val_04():
    """U-VAL-04 — 5x5 행렬 → E001."""
    grid = [[0] * 5] * 5
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE


def test_validator_rejects_empty_list_u_val_05():
    """U-VAL-05 — 빈 리스트 → E001."""
    result = InputValidator.validate([])
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_SIZE


# ---------------------------------------------------------------------------
# U-VAL-06~08 — I2 빈칸 개수 (E002 INVALID_BLANK_COUNT)
# ---------------------------------------------------------------------------
def test_validator_rejects_zero_blanks_u_val_06(durer_grid):
    """U-VAL-06 — 4x4이며 0이 0개 → E002."""
    result = InputValidator.validate(durer_grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_BLANK_COUNT
    assert result.error.message == "Grid must contain exactly 2 blank cells (0)."


def test_validator_rejects_one_blank_u_val_07(durer_grid):
    """U-VAL-07 — 4x4이며 0이 1개 → E002."""
    grid = [row[:] for row in durer_grid]
    grid[0][0] = 0  # 빈칸 1개
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_BLANK_COUNT


def test_validator_rejects_three_blanks_u_val_08(durer_grid):
    """U-VAL-08 — 4x4이며 0이 3개 → E002."""
    grid = [row[:] for row in durer_grid]
    grid[0][0] = 0
    grid[1][1] = 0
    grid[2][2] = 0
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_BLANK_COUNT


# ---------------------------------------------------------------------------
# U-VAL-09~10 — I3 값 범위 (E003 INVALID_VALUE_RANGE)
# ---------------------------------------------------------------------------
def test_validator_rejects_negative_value_u_val_09():
    """U-VAL-09 — -1 포함 → E003."""
    grid = [
        [-1, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_VALUE_RANGE
    assert result.error.message == "All values must be in [0, 16]."


def test_validator_rejects_value_above_16_u_val_10():
    """U-VAL-10 — 17 포함 → E003."""
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 17],
        [4, 15, 14, 0],
    ]
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.INVALID_VALUE_RANGE


# ---------------------------------------------------------------------------
# U-VAL-11 — I4 0 제외 중복 (E004 DUPLICATE_VALUE)
# ---------------------------------------------------------------------------
def test_validator_rejects_duplicate_nonzero_u_val_11():
    """U-VAL-11 — 0이 아닌 값이 중복(5가 두 번) → E004."""
    grid = [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 5, 12],  # 5 중복
        [4, 15, 14, 0],
    ]
    result = InputValidator.validate(grid)
    assert result.is_error is True
    assert result.error.code == ErrorCode.DUPLICATE_VALUE
    assert result.error.message == "Non-zero values must be unique."


# ---------------------------------------------------------------------------
# U-FLOW-01~02 — I12 흐름 (invalid 입력 시 Domain 호출 0회)
# ---------------------------------------------------------------------------
def test_valid_input_calls_domain_once_u_flow_01(partial_step_a_grid):
    """U-FLOW-01 — 유효 입력 시 Domain Service가 정확히 1회 호출됨."""
    # Arrange — Boundary는 Solver mock을 주입받아 호출 횟수만 검증
    solver_mock = MagicMock()
    validator_chain = InputValidator(solver=solver_mock)

    # Act
    validator_chain.solve(partial_step_a_grid)

    # Assert
    assert solver_mock.solve.call_count == 1


def test_invalid_input_does_not_call_domain_u_flow_02():
    """U-FLOW-02 — invalid 입력 시 Domain Service 호출 0회 (I12)."""
    # Arrange — 4x4 아닌 입력
    solver_mock = MagicMock()
    validator_chain = InputValidator(solver=solver_mock)
    invalid_grid = [[1, 2, 3]]  # 1x3

    # Act
    validator_chain.solve(invalid_grid)

    # Assert
    assert solver_mock.solve.call_count == 0

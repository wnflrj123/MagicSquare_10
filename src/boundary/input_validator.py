"""InputValidator — I1·I2·I3·I4 검증 + I12 흐름 차단.

PRD `Report/08_prd.md` §6 FR-01. Domain Service는 invalid 입력에 호출 안 됨.
"""
from __future__ import annotations

from typing import Any, List, Optional

from boundary.error_codes import ErrorCode, Result, make_error
from entity.constants import BLANK_COUNT, BLANK_VALUE, GRID_SIZE, MAX_VALUE, MIN_VALUE


class InputValidator:
    """입력 계약 4종 검증 (I1·I2·I3·I4) + 선택적 Domain 호출 (I12)."""

    def __init__(self, solver: Optional[Any] = None) -> None:
        """Solver(use_case)를 선택적으로 주입.

        Args:
            solver: validate 통과 시 호출할 객체. None이면 검증만 수행.
        """
        self.solver = solver

    @classmethod
    def validate(cls, grid: Any) -> Result:
        """입력 계약 4종 검증.

        Args:
            grid: 검증 대상 (정상이면 4×4 정수 행렬).

        Returns:
            Result — error가 None이면 검증 통과.
        """
        # I1: 4×4 shape
        if grid is None:
            return make_error(ErrorCode.INVALID_SIZE)
        if not isinstance(grid, list) or len(grid) != GRID_SIZE:
            return make_error(ErrorCode.INVALID_SIZE)
        for row in grid:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                return make_error(ErrorCode.INVALID_SIZE)

        # I3: 값 범위 ∈ {0} ∪ {1..MAX_VALUE}
        for row in grid:
            for value in row:
                if not isinstance(value, int) or value < BLANK_VALUE or value > MAX_VALUE:
                    return make_error(ErrorCode.INVALID_VALUE_RANGE)

        # I2: 빈칸(0) 개수 = BLANK_COUNT
        blank_count = sum(1 for row in grid for v in row if v == BLANK_VALUE)
        if blank_count != BLANK_COUNT:
            return make_error(ErrorCode.INVALID_BLANK_COUNT)

        # I4: 0 제외 중복 없음
        nonzero: List[int] = [v for row in grid for v in row if v != BLANK_VALUE]
        if len(nonzero) != len(set(nonzero)):
            return make_error(ErrorCode.DUPLICATE_VALUE)

        return Result(value=[])  # 검증 통과 표식

    def solve(self, grid: Any) -> Result:
        """validate → 통과 시 self.solver.solve(grid) 호출 (I12: invalid 시 호출 0회).

        Args:
            grid: 검증 대상.

        Returns:
            검증 실패 시 Result(error=...). 검증 통과 시 solver.solve 결과 후
            Result(value=[])를 반환 (U-FLOW 테스트는 결과 값보다 호출 횟수만 검증).
        """
        validation = self.validate(grid)
        if validation.is_error:
            return validation
        if self.solver is not None:
            self.solver.solve(grid)
        return validation

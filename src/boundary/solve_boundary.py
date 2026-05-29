"""SolveBoundary — 외부 호출자에게 통합 진입점 제공.

PRD `Report/08_prd.md` §6 FR-08. InputValidator → use_case → Result 변환.
"""
from __future__ import annotations

from typing import Any, List

from boundary.error_codes import ErrorCode, Result, make_error
from boundary.input_validator import InputValidator
from entity.errors import NoValidMagicSquareError


class SolveBoundary:
    """입력 검증 + use_case 호출 + 도메인 실패(E005) 변환."""

    def __init__(self, use_case: Any) -> None:
        """Use Case(또는 mock)를 주입.

        Args:
            use_case: `.solve(grid) -> int[6]` 인터페이스를 만족하는 객체.
        """
        self.use_case = use_case

    def solve(self, grid: Any) -> Result:
        """검증 → 호출 → 결과 변환.

        Args:
            grid: 외부에서 전달된 입력.

        Returns:
            Result — 성공: value=int[6] / 실패: error=E001~E005.
        """
        validation = InputValidator.validate(grid)
        if validation.is_error:
            return validation
        try:
            value: List[int] = self.use_case.solve(grid)
            return Result(value=value)
        except NoValidMagicSquareError:
            return make_error(ErrorCode.NO_VALID_MAGIC_SQUARE)

"""Boundary 에러 코드 + Result 타입.

PRD `Report/08_prd.md` §8 에러 코드 SSOT. 메시지는 문자 단위 동등 비교 대상.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ErrorCode(Enum):
    """정의된 에러 코드 5종 (E001~E005)."""

    INVALID_SIZE = "E001"
    INVALID_BLANK_COUNT = "E002"
    INVALID_VALUE_RANGE = "E003"
    DUPLICATE_VALUE = "E004"
    NO_VALID_MAGIC_SQUARE = "E005"


# 코드 ↔ (분류, 메시지) SSOT. PRD §8.
_ERROR_REGISTRY = {
    ErrorCode.INVALID_SIZE: ("INPUT_ERROR", "Grid must be 4x4."),
    ErrorCode.INVALID_BLANK_COUNT: (
        "INPUT_ERROR",
        "Grid must contain exactly 2 blank cells (0).",
    ),
    ErrorCode.INVALID_VALUE_RANGE: ("INPUT_ERROR", "All values must be in [0, 16]."),
    ErrorCode.DUPLICATE_VALUE: ("INPUT_ERROR", "Non-zero values must be unique."),
    ErrorCode.NO_VALID_MAGIC_SQUARE: ("DOMAIN_FAILURE", "No valid magic square found."),
}


@dataclass(frozen=True)
class ErrorObject:
    """에러 응답 객체.

    Args:
        code: ErrorCode enum (E001~E005).
        message: 정문구 (PRD §8 SSOT, 문자 단위 동등).
        type: "INPUT_ERROR" 또는 "DOMAIN_FAILURE".
    """

    code: ErrorCode
    message: str
    type: str


@dataclass(frozen=True)
class Result:
    """Boundary 응답 타입 — 성공 또는 에러.

    Args:
        value: 성공 시 int[6] (또는 검증 통과 표식의 빈 리스트).
        error: 실패 시 ErrorObject.
    """

    value: Optional[List[int]] = None
    error: Optional[ErrorObject] = None

    @property
    def is_ok(self) -> bool:
        """에러가 없으면 성공."""
        return self.error is None

    @property
    def is_error(self) -> bool:
        """에러가 있으면 실패."""
        return self.error is not None


def make_error(code: ErrorCode) -> Result:
    """주어진 코드로 Result(error=...) 를 생성한다.

    Args:
        code: ErrorCode enum.

    Returns:
        Result(error=ErrorObject(...)) — message·type은 SSOT 레지스트리에서.
    """
    error_type, message = _ERROR_REGISTRY[code]
    return Result(error=ErrorObject(code=code, message=message, type=error_type))

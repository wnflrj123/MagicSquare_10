"""Value Objects — 불변·비교 가능한 도메인 값 객체.

PRD `Report/08_prd.md` §5 출력 계약 + `Report/04_architecture_design.md` §1.1.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    """격자 한 칸의 위치. 좌표는 1-index (I10).

    Args:
        row: 행 (1..GRID_SIZE).
        col: 열 (1..GRID_SIZE).
    """

    row: int
    col: int


@dataclass(frozen=True)
class MissingPair:
    """누락된 두 수 (작은 수 먼저, I8 전제).

    Args:
        n_small: 작은 누락 수.
        n_big: 큰 누락 수 (n_small < n_big).
    """

    n_small: int
    n_big: int

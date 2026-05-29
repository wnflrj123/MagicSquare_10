"""MissingNumberFinder — {1..16} − 격자값 = 누락 두 수.

PRD `Report/08_prd.md` §6 FR-03. I8 (작은 수 먼저 정렬).
"""
from __future__ import annotations

from typing import List

from entity.constants import BLANK_VALUE, MAX_VALUE, MIN_VALUE
from entity.value_objects import MissingPair


class MissingNumberFinder:
    """{MIN_VALUE..MAX_VALUE}에서 격자에 등장한 값을 뺀 차집합 = 누락 두 수."""

    @staticmethod
    def find(grid: List[List[int]]) -> MissingPair:
        """누락된 두 수를 (작은 수, 큰 수) 순서로 반환.

        Args:
            grid: 4×4 정수 행렬. 0이 빈칸.

        Returns:
            MissingPair (n_small < n_big).
        """
        present = {v for row in grid for v in row if v != BLANK_VALUE}
        missing = sorted(set(range(MIN_VALUE, MAX_VALUE + 1)) - present)
        return MissingPair(n_small=missing[0], n_big=missing[1])

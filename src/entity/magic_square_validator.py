"""MagicSquareValidator — 완성된 4×4 격자가 마방진인지 판정 (I5·I6).

PRD `Report/08_prd.md` §6 FR-04.
"""
from __future__ import annotations

from typing import List

from entity.constants import GRID_SIZE, MAGIC_CONSTANT


class MagicSquareValidator:
    """모든 행/열/대각선 합 = MAGIC_CONSTANT 여야 마방진."""

    @staticmethod
    def is_magic(grid: List[List[int]]) -> bool:
        """주어진 격자가 마방진인지 판정.

        Args:
            grid: 4×4 정수 행렬 (완성형 가정).

        Returns:
            True if 모든 행/열/대각선 합이 MAGIC_CONSTANT.
        """
        # 모든 행
        for row in grid:
            if sum(row) != MAGIC_CONSTANT:
                return False
        # 모든 열
        for c in range(GRID_SIZE):
            if sum(grid[r][c] for r in range(GRID_SIZE)) != MAGIC_CONSTANT:
                return False
        # 주대각선
        if sum(grid[i][i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False
        # 부대각선
        if sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)) != MAGIC_CONSTANT:
            return False
        return True

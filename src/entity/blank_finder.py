"""BlankFinder — 빈칸 좌표를 row-major 순서로 찾는다 (I7).

PRD `Report/08_prd.md` §6 FR-02.
"""
from __future__ import annotations

from typing import List

from entity.constants import BLANK_VALUE, GRID_SIZE
from entity.value_objects import Coordinate


class BlankFinder:
    """격자의 빈칸 좌표를 1-index, row-major 순서로 반환."""

    @staticmethod
    def find(grid: List[List[int]]) -> List[Coordinate]:
        """row-major 스캔으로 빈칸(0) 좌표를 모두 반환한다.

        Args:
            grid: 4×4 정수 행렬. 0이 빈칸.

        Returns:
            Coordinate 리스트 (1-index, row-major 순서).
        """
        result: List[Coordinate] = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if grid[r][c] == BLANK_VALUE:
                    result.append(Coordinate(row=r + 1, col=c + 1))
        return result

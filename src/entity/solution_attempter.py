"""SolutionAttempter — 두 빈칸에 (n_a, n_b)를 배치한 새 격자 반환 (순수 함수).

PRD `Report/08_prd.md` §6 FR-05. 입력 불변·결정성.
"""
from __future__ import annotations

from typing import List, Tuple

from entity.value_objects import Coordinate


class SolutionAttempter:
    """주어진 빈칸 좌표에 두 수를 배치한 새 격자를 반환."""

    @staticmethod
    def apply(
        grid: List[List[int]],
        blanks: List[Coordinate],
        pair: Tuple[int, int],
    ) -> List[List[int]]:
        """blanks[0] ← pair[0], blanks[1] ← pair[1] 인 새 격자 반환.

        Args:
            grid: 원본 4×4 격자 (불변).
            blanks: 두 빈칸 좌표 (1-index).
            pair: 배치할 두 수 (첫 빈칸용, 둘째 빈칸용).

        Returns:
            새 4×4 격자 (입력 불변, 깊은 복사).
        """
        new_grid = [row[:] for row in grid]
        n_a, n_b = pair
        new_grid[blanks[0].row - 1][blanks[0].col - 1] = n_a
        new_grid[blanks[1].row - 1][blanks[1].col - 1] = n_b
        return new_grid

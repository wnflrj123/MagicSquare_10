"""StepABSolver — Step A 우선 → 실패 시 Step B (reverse) → 둘 다 실패 시 예외.

PRD `Report/08_prd.md` §6 FR-06. I7·I8·I9·I10·I11 보호.
"""
from __future__ import annotations

from typing import List

from entity.blank_finder import BlankFinder
from entity.errors import NoValidMagicSquareError
from entity.magic_square_validator import MagicSquareValidator
from entity.missing_number_finder import MissingNumberFinder
from entity.solution_attempter import SolutionAttempter


class StepABSolver:
    """Step A → Step B 오케스트레이션."""

    @staticmethod
    def solve(grid: List[List[int]]) -> List[int]:
        """부분 마방진을 풀어 int[6] 반환.

        Args:
            grid: 4×4 정수 행렬 (빈칸 2개, Boundary 검증 통과 가정).

        Returns:
            int[6] = [r1, c1, n1, r2, c2, n2] (1-index, row-major 빈칸 순서).
            Step A 성공 시 n1 < n2, Step B 성공 시 n1 > n2.

        Raises:
            NoValidMagicSquareError: Step A·B 모두 실패 (I11).
        """
        blanks = BlankFinder.find(grid)
        pair = MissingNumberFinder.find(grid)
        r1, c1 = blanks[0].row, blanks[0].col
        r2, c2 = blanks[1].row, blanks[1].col

        # I8 → I9 우선순위: Step A((small,big))를 먼저, 실패 시 Step B((big,small))
        for n_first, n_second in [(pair.n_small, pair.n_big), (pair.n_big, pair.n_small)]:
            attempt = SolutionAttempter.apply(grid, blanks, (n_first, n_second))
            if MagicSquareValidator.is_magic(attempt):
                return [r1, c1, n_first, r2, c2, n_second]

        raise NoValidMagicSquareError("No valid magic square found.")

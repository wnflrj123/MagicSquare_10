"""SolvePartialMagicSquare — Use Case orchestration.

PRD `Report/08_prd.md` §6 FR-07. Boundary로부터 검증된 입력을 받아 Domain
Service(StepABSolver) 호출만 위임한다.
"""
from __future__ import annotations

from typing import List

from entity.step_ab_solver import StepABSolver


class SolvePartialMagicSquare:
    """Boundary로부터 검증 통과한 부분 마방진을 받아 풀이를 위임."""

    def resolve(self, grid: List[List[int]]) -> List[int]:
        """부분 마방진을 풀어 int[6] 반환.

        Args:
            grid: Boundary 검증 통과한 4×4 부분 마방진.

        Returns:
            int[6] = [r1, c1, n1, r2, c2, n2].

        Raises:
            NoValidMagicSquareError: Step A·B 모두 실패.
        """
        return StepABSolver.solve(grid)

    def solve(self, grid: List[List[int]]) -> List[int]:
        """SolveBoundary.use_case.solve(grid) 인터페이스 별칭."""
        return self.resolve(grid)

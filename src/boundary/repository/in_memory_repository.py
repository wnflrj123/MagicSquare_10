"""InMemoryRepository — 메모리 dict 기반 격자 영속성.

PRD `Report/08_prd.md` §6 FR-09 보조. Repository 계약(DAT-CONTRACT-*)을 만족하는
가장 간단한 구현. File 구현은 Golden Master 단계에서 추가.
"""
from __future__ import annotations

from typing import Dict, List


class InMemoryRepository:
    """프로세스 메모리(dict)에 격자를 저장·로드한다."""

    def __init__(self) -> None:
        """저장소 인스턴스마다 독립된 dict 보유 (테스트 간 격리)."""
        self._inputs: Dict[str, List[List[int]]] = {}

    def save_input(self, identifier: str, grid: List[List[int]]) -> None:
        """격자를 식별자로 저장.

        Args:
            identifier: 저장 식별자.
            grid: 4×4 정수 행렬.

        Raises:
            ValueError: 동일 identifier가 이미 존재 (DUPLICATE_ID).
        """
        if identifier in self._inputs:
            raise ValueError(f"Duplicate id: {identifier}")
        self._inputs[identifier] = [row[:] for row in grid]

    def load_input(self, identifier: str) -> List[List[int]]:
        """식별자로 격자를 로드.

        Args:
            identifier: 저장 식별자.

        Returns:
            저장 시점의 4×4 격자 (얕은 복사로 외부 변형 격리).

        Raises:
            KeyError: identifier 미존재 (NOT_FOUND).
        """
        if identifier not in self._inputs:
            raise KeyError(f"Not found: {identifier}")
        return [row[:] for row in self._inputs[identifier]]

    def exists(self, identifier: str) -> bool:
        """저장 여부 확인.

        Args:
            identifier: 저장 식별자.

        Returns:
            True if save_input 으로 저장된 적 있음.
        """
        return identifier in self._inputs

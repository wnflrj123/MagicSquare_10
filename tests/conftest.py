"""공통 픽스처 + pytest 플러그인 옵션.

PRD `Report/08_prd.md` §13 Traceability + Report/09 §5 정합.
"""
from __future__ import annotations
from typing import List

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Golden Master baseline 재생성 플래그.

    사용:
        pytest                          # 비교 모드 (회귀 검출)
        pytest --approve-golden         # baseline 재생성 (의도적 변경 수용)
    """
    parser.addoption(
        "--approve-golden",
        action="store_true",
        default=False,
        help="Regenerate Golden Master baseline file(s) instead of comparing.",
    )


GridT = List[List[int]]


# 09 §5.1 Dürer 4×4 마방진 — 행/열/대각선 합 = 34
DURER_MAGIC_SQUARE: GridT = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# 09 §5.2 부분 마방진 — Step A 성공 케이스
# Dürer에서 (1,3)=2, (3,1)=9 를 0으로 가린 입력. 누락 {2,9}, 작은수→첫 빈칸
PARTIAL_STEP_A_GRID: GridT = [
    [16, 3, 0, 13],
    [5, 10, 11, 8],
    [0, 6, 7, 12],
    [4, 15, 14, 1],
]
PARTIAL_STEP_A_EXPECTED_RESULT = [1, 3, 2, 3, 1, 9]  # [r1,c1,n1,r2,c2,n2] 1-index

# 09 §5.3 부분 마방진 — Step B (reverse) 성공 케이스
# Dürer에서 (1,1)=16, (4,4)=1 을 0으로 가린 입력. Step A 실패 → Step B 성공
PARTIAL_STEP_B_GRID: GridT = [
    [0, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 0],
]
PARTIAL_STEP_B_EXPECTED_RESULT = [1, 1, 16, 4, 4, 1]

# 09 §5.4 풀 수 없는 입력 — E005 NO_VALID_MAGIC_SQUARE 유발
# 빈칸 (2,4)·(3,3), 누락 {8, 11}, Step A·B 모두 실패
UNSOLVABLE_GRID: GridT = [
    [1, 2, 3, 4],
    [5, 6, 7, 0],
    [9, 10, 0, 12],
    [13, 14, 15, 16],
]


@pytest.fixture
def durer_grid() -> GridT:
    """Dürer 마방진 (완성형) — D-VAL-01 정답 baseline."""
    return [row[:] for row in DURER_MAGIC_SQUARE]


@pytest.fixture
def partial_step_a_grid() -> GridT:
    """Step A로 풀리는 부분 마방진."""
    return [row[:] for row in PARTIAL_STEP_A_GRID]


@pytest.fixture
def partial_step_b_grid() -> GridT:
    """Step B (reverse)로만 풀리는 부분 마방진."""
    return [row[:] for row in PARTIAL_STEP_B_GRID]


@pytest.fixture
def unsolvable_grid() -> GridT:
    """Step A·B 모두 실패하는 부분 마방진."""
    return [row[:] for row in UNSOLVABLE_GRID]

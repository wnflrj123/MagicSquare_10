"""Domain constants (SSOT).

PRD `Report/08_prd.md` §6 FR-04, `Report/04_architecture_design.md` §0,
`.cursorrules` code_style.literal_constants 정합. 본 모듈만이 격자 크기·
Magic Constant 의 출처(Single Source of Truth)다.
"""
from __future__ import annotations


GRID_SIZE: int = 4
BLANK_VALUE: int = 0
MIN_VALUE: int = 1
MAX_VALUE: int = GRID_SIZE * GRID_SIZE  # 16
BLANK_COUNT: int = 2
OUTPUT_LENGTH: int = BLANK_COUNT * 3  # 6 = [r, c, n] x 2

# I5: 1+2+...+MAX_VALUE = MAX_VALUE*(MAX_VALUE+1)/2 = 136. 한 줄의 합 = 136/4 = 34.
MAGIC_CONSTANT: int = (MAX_VALUE * (MAX_VALUE + 1) // 2) // GRID_SIZE

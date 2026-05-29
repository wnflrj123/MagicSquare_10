"""Domain exceptions.

Boundary가 정의된 에러 코드(E005)로 변환한다. `Report/08_prd.md` §8.
"""
from __future__ import annotations


class NoValidMagicSquareError(Exception):
    """Step A·B 모두 마방진을 만들지 못함 (I11).

    Boundary가 본 예외를 catch 하여 `E005 NO_VALID_MAGIC_SQUARE` 로 변환.
    """

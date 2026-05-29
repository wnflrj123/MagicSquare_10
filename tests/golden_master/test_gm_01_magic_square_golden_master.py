"""I-GM-01 — Magic Square Golden Master 회귀 잠금 테스트.

PRD `Report/08_prd.md` §11 회귀 잠금 L7 활성화, 워크북 L5048~5276 정렬.

baseline 파일: tests/golden_master/golden_master_expected.json
입력 케이스: GOLDEN_MASTER_CASES (8건 — 성공·실패·입력에러 전 시나리오 커버)

명령:
    pytest tests/golden_master/ -v                     # 비교 (회귀 검출)
    pytest tests/golden_master/ -v --approve-golden    # baseline 재생성

회귀 발생 시 (예: int[6] 형식 변경·에러 메시지 변경 등):
    1. 변경이 의도적이라면 `--approve-golden`으로 baseline 갱신 (별도 PR)
    2. 의도하지 않은 변경이라면 production 코드 수정으로 baseline 복원
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from boundary.error_codes import Result
from boundary.solve_boundary import SolveBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare


BASELINE_PATH: Path = Path(__file__).parent / "golden_master_expected.json"


# Golden Master 케이스 — 12 invariant·5 에러 코드·Step A/B 전부 커버
GOLDEN_MASTER_CASES: List[Dict[str, Any]] = [
    {
        "id": "GM-TC-01",
        "name": "step_a_durer_missing_2_and_9",
        "description": "Dürer 마방진에서 (1,3)=2·(3,1)=9 가린 부분 마방진 → Step A 성공",
        "input": [
            [16, 3, 0, 13],
            [5, 10, 11, 8],
            [0, 6, 7, 12],
            [4, 15, 14, 1],
        ],
    },
    {
        "id": "GM-TC-02",
        "name": "step_b_reverse_durer_missing_16_and_1",
        "description": "Dürer 마방진에서 (1,1)=16·(4,4)=1 가린 부분 → Step A 실패·Step B 성공",
        "input": [
            [0, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ],
    },
    {
        "id": "GM-TC-03",
        "name": "unsolvable_both_steps_fail",
        "description": "Step A·B 모두 마방진 못 만드는 입력 → E005 NO_VALID_MAGIC_SQUARE",
        "input": [
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [9, 10, 0, 12],
            [13, 14, 15, 16],
        ],
    },
    {
        "id": "GM-TC-04",
        "name": "invalid_size_3x4",
        "description": "3x4 행렬 → E001 INVALID_SIZE (Domain 호출 0회)",
        "input": [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ],
    },
    {
        "id": "GM-TC-05",
        "name": "invalid_blank_count_zero_blanks",
        "description": "Dürer 완성형(빈칸 0개) → E002 INVALID_BLANK_COUNT",
        "input": [
            [16, 3, 2, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 1],
        ],
    },
    {
        "id": "GM-TC-06",
        "name": "invalid_value_range_negative",
        "description": "-1 포함 → E003 INVALID_VALUE_RANGE",
        "input": [
            [-1, 3, 0, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 12],
            [4, 15, 14, 0],
        ],
    },
    {
        "id": "GM-TC-07",
        "name": "invalid_value_range_above_max",
        "description": "17 포함 → E003 INVALID_VALUE_RANGE",
        "input": [
            [16, 3, 0, 13],
            [5, 10, 11, 8],
            [9, 6, 7, 17],
            [4, 15, 14, 0],
        ],
    },
    {
        "id": "GM-TC-08",
        "name": "duplicate_value_5_twice",
        "description": "0 제외 중복(5가 두 번) → E004 DUPLICATE_VALUE",
        "input": [
            [16, 3, 0, 13],
            [5, 10, 11, 8],
            [9, 6, 5, 12],
            [4, 15, 14, 0],
        ],
    },
]


def _serialize_result(result: Result) -> Dict[str, Any]:
    """Result 객체를 JSON 직렬화 가능한 dict로 변환 (baseline 비교용)."""
    if result.is_ok:
        return {"ok": True, "value": result.value}
    assert result.error is not None  # is_ok=False → error 존재
    return {
        "ok": False,
        "error": {
            "code": result.error.code.value,
            "type": result.error.type,
            "message": result.error.message,
        },
    }


def _execute_all_cases() -> List[Dict[str, Any]]:
    """모든 GM 케이스를 production composition으로 실행해 직렬화된 baseline 생성."""
    boundary = SolveBoundary(use_case=SolvePartialMagicSquare())
    return [
        {
            "id": case["id"],
            "name": case["name"],
            "description": case["description"],
            "input": case["input"],
            "expected": _serialize_result(boundary.solve(case["input"])),
        }
        for case in GOLDEN_MASTER_CASES
    ]


def test_golden_master_baseline_matches_i_gm_01(request: pytest.FixtureRequest) -> None:
    """I-GM-01 — 모든 GM 케이스 출력이 baseline 파일과 정확히 일치.

    Args:
        request: pytest fixture (--approve-golden CLI 옵션 접근용).

    Raises:
        AssertionError: 회귀 발생 (출력이 baseline과 다름).
        pytest.fail: baseline 파일 미존재 (--approve-golden으로 생성 필요).

    Side effect (--approve-golden 시):
        BASELINE_PATH에 현재 실행 결과를 baseline으로 기록.
    """
    actual = _execute_all_cases()

    if request.config.getoption("--approve-golden"):
        BASELINE_PATH.write_text(
            json.dumps(actual, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        pytest.skip(
            f"Baseline 재생성: {len(actual)}건 → {BASELINE_PATH.name}"
        )

    if not BASELINE_PATH.exists():
        pytest.fail(
            f"Baseline 파일 없음: {BASELINE_PATH}\n"
            f"최초 생성: pytest tests/golden_master/ --approve-golden"
        )

    expected = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    assert actual == expected, (
        "Golden Master 회귀 발생: production 출력이 baseline과 다름.\n"
        "의도적 변경이면 별도 PR로 --approve-golden 갱신."
    )

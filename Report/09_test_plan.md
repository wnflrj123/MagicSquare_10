# Test Plan — Magic Square 4×4 Partial Solver

> 작성일: 2026-05-29
> 단계: M1 (Test Plan + RED Skeleton) — 워크북 §"테스트 플랜" (L3876~3938) + §"테스트 케이스 작성" (L3961~3989) + §"RED Skeleton" (L4414~4456) 산출물
> 작업 브랜치: `feature/red-skeleton` → `develop` PR 예정 (A1 카덴스, 02 §2.3)
> 전제 문서: [`Report/08_prd.md`](./08_prd.md) §6 FR + §8 에러 코드 + §13 Traceability

---

## 1. 본 단계의 목표

워크북 L4197 PR 시점 ("Compare & pull request" — RED 테스트 플랜 완성 후)에 도달하기 위한 **RED Skeleton 일괄 작성**.

본 단계의 산출은 다음 조건을 모두 만족해야 한다:

- [x] PRD §13 Traceability의 모든 테스트 ID가 실제 테스트 파일·함수로 존재
- [x] `pytest`가 정상 수집 (수집 에러 0건 또는 의도된 ImportError만)
- [x] 모든 테스트가 RED 상태 (의도된 실패 + 우연한 통과 0건)
- [x] 다음 GREEN 단계는 production 코드 추가만으로 각 테스트를 통과시킬 수 있어야 한다

---

## 2. RED Skeleton 작성 방식 결정

워크북 L4414~4421은 두 가지 패턴 중 후자(`pytest.fail()`만)를 권장:

```
1. 테스트 파일·클래스·함수·fixture 구조만 작성
2. 각 테스트 본문은 의도적 실패 한 줄만: pytest.fail("not implemented")
3. production import는 허용 (Report/08과 동일)
4. Arrange/Act 코드는 주석으로만 표시 가능
5. Then 검증은 작성하지 않음 — pytest.fail()만
```

본 프로젝트는 **다른 패턴을 채택**한다 (근거 설명 후 결정):

### 채택 패턴: 완전한 테스트 + production import → ImportError로 RED

```python
from entity.blank_finder import BlankFinder  # ← RED: 모듈 없음 → ImportError

def test_blank_finder_returns_row_major_order():
    """D-LOC-01 — 빈칸 좌표는 row-major 순서."""
    # Arrange
    grid = [[0,1,2,3], ...]
    # Act
    coords = BlankFinder.find(grid)
    # Assert
    assert coords == [Coordinate(1,1), Coordinate(4,4)]
```

### 채택 근거

| 항목 | 워크북 `pytest.fail()` 스타일 | 본 프로젝트 `ImportError` 스타일 |
| --- | --- | --- |
| RED 상태 도달 | ✅ pytest 본문에서 실패 | ✅ 수집 단계에서 ImportError (= feature missing) |
| GREEN 단계 변경 범위 | 테스트 본문 + production 코드 (2곳) | production 코드만 (1곳) |
| 02 §3.2 핵심 규칙 4 ("Refactor/GREEN 단계에서 기존 테스트 변경 금지") | ⚠️ 위반 가능성 — pytest.fail을 assertion으로 교체하면 변경 | ✅ 테스트는 RED부터 GREEN까지 그대로 |
| 테스트 가독성 | 낮음 (본문이 fail 한 줄) | 높음 (실제 의도가 보임) |

> **결정**: 본 프로젝트는 우리 02 §3.2의 "GREEN 단계에서 기존 테스트 변경 금지" 규칙을 더 우선시한다. ImportError 기반 RED는 워크북의 RED 기준("feature missing")도 정확히 만족한다 (`02_branching_strategy.md` §3.2 + `superpowers:test-driven-development` 스킬의 "Test errors? Fix error, re-run until it fails correctly" 가이드 정합).

---

## 3. 테스트 파일 매핑 (PRD §13 정합)

| Test ID 범위 | 파일 | 보호 invariant | FR |
| --- | --- | --- | --- |
| D-LOC-01~03 | `tests/entity/test_blank_finder.py` | I7 | FR-02 |
| D-MISS-01~03 | `tests/entity/test_missing_number_finder.py` | I8 (정렬 부분) | FR-03 |
| D-VAL-01~06 | `tests/entity/test_magic_square_validator.py` | I5·I6 | FR-04 |
| D-ATT-01~02 | `tests/entity/test_solution_attempter.py` | (순수성) | FR-05 |
| D-SOL-01~06 | `tests/entity/test_step_ab_solver.py` | I8·I9·I10·I11 | FR-06 |
| U-VAL-01~11, U-FLOW-01~02 | `tests/boundary/test_input_validator.py` | I1·I2·I3·I4·I12 | FR-01 |
| U-OUT-01~03 | `tests/boundary/test_solve_boundary.py` | I10·I11 | FR-08 |
| C-SOL-01~02 | `tests/control/test_solve_partial_magic_square.py` | (오케스트레이션) | FR-07 |
| I-INT-01~07 | `tests/integration/test_end_to_end.py` | 전체 | FR-01~FR-08 |
| DAT-MEM-01~05 | `tests/data/test_in_memory_repository.py` | (영속성 계약) | FR-09 보조 |

총: **10개 파일 + 약 50개 테스트 함수**.

> `D-VAL-07` (Magic Constant SSOT 정적 분석)은 pytest 대상이 아님 — 별도 lint 또는 `ruff` rule로 추후 처리.

---

## 4. 픽스처 정책

| 픽스처 | 위치 | 범위 | 사유 |
| --- | --- | --- | --- |
| `MAGIC_SQUARE_GRID` (Dürer 4×4 마방진) | `tests/conftest.py` 또는 각 파일 | session | 여러 D-VAL·D-SOL 테스트에서 재사용. 변경 불가 상수 |
| `VALID_PARTIAL_GRID_STEP_A` | 픽스처 | function | Step A로 풀리는 입력 |
| `VALID_PARTIAL_GRID_STEP_B` | 픽스처 | function | Step B (reverse)로만 풀리는 입력 |
| `UNSOLVABLE_PARTIAL_GRID` | 픽스처 | function | Step A·B 모두 실패 입력 |

**M1 RED 단계에서는 픽스처는 인라인으로 작성**한다 (각 테스트 본문의 Arrange 단락). 공통 픽스처 추출은 M2 GREEN 후 REFACTOR 단계로 미룬다.

---

## 5. 도메인 사실 — 본 Test Plan이 정착하는 표본

### 5.1 Dürer 4×4 마방진 (검증용 baseline)

```
16  3  2 13
 5 10 11  8
 9  6  7 12
 4 15 14  1
```

검증:
- 행: 16+3+2+13=34, 5+10+11+8=34, 9+6+7+12=34, 4+15+14+1=34 ✓
- 열: 16+5+9+4=34, 3+10+6+15=34, 2+11+7+14=34, 13+8+12+1=34 ✓
- 주대각선: 16+10+7+1=34 ✓
- 부대각선: 13+11+6+4=34 ✓

### 5.2 부분 마방진 표본 — Step A 성공

Dürer 마방진에서 (1,3)=2 와 (3,1)=9 를 0으로 가린 입력:

```
16  3  0 13      누락: {2, 9}
 5 10 11  8      Step A: 작은수(2)→첫 빈칸(1,3), 큰수(9)→둘째(3,1)
 0  6  7 12      배치 결과: Dürer 마방진 그대로
 4 15 14  1      → Step A 성공
```

기대 출력: `[1, 3, 2, 3, 1, 9]`

### 5.3 부분 마방진 표본 — Step B (reverse) 성공

Dürer 마방진에서 (1,1)=16 과 (4,4)=1 을 0으로 가린 입력:

```
 0  3  2 13      누락: {1, 16}
 5 10 11  8      Step A: 작은수(1)→(1,1), 큰수(16)→(4,4)
 9  6  7 12         → 행 합 (1+3+2+13)=19 ≠ 34 → 실패
 4 15 14  0      Step B: 큰수(16)→(1,1), 작은수(1)→(4,4)
                    → Dürer 마방진 → 성공
```

기대 출력: `[1, 1, 16, 4, 4, 1]`

### 5.4 풀 수 없는 입력 표본 (E005)

```
1 2 3 4
5 6 7 0
9 10 0 12
13 14 15 16    빈칸: (2,4)·(3,3), 누락: {8, 11}
```

확인:
- Step A: 8→(2,4), 11→(3,3) → 행2: 5+6+7+8=26 ≠ 34 → 실패
- Step B: 11→(2,4), 8→(3,3) → 행2: 5+6+7+11=29 ≠ 34 → 실패
- → E005 NO_VALID_MAGIC_SQUARE

---

## 6. 실행 명령

```bash
# RED skeleton 작성 직후 (수집 + 실행)
.venv/bin/python -m pytest -v

# 기대 결과 (RED 상태):
# - tests/entity/test_user.py::test_user_creation_stores_id_name_email PASSED (워밍업, 06)
# - 나머지 모든 새 테스트: ERROR (ImportError, module not found)
# - 또는 ERROR (collection error)

# RED 확인용 명령
.venv/bin/python -m pytest --collect-only 2>&1 | grep -E '(ERROR|error)'
```

---

## 7. RED 완료 (Definition of Done)

본 M1 단계가 완료된 것으로 인정되는 조건:

- [ ] 본 문서가 develop에 머지됨
- [ ] `tests/` 의 10개 파일·약 50개 테스트가 작성됨
- [ ] `pytest` 실행 시:
  - 워밍업 1건만 PASS
  - 나머지는 모두 ERROR(ImportError) 또는 FAIL(의도적)
  - typo·구문 오류 0건
- [ ] PRD §13 Traceability 모든 행이 실제 테스트 ID와 매핑됨
- [ ] PR feature/red-skeleton → develop 머지 (A1 카덴스)

---

## 8. 다음 단계 (M2 GREEN 이후)

A1 PR 머지 후:
- M2 GREEN — InputValidator: `feature/bnd-input-validator` 브랜치, U-VAL-* + U-FLOW-* 통과
- M3 GREEN — Domain Services: 각 D-* 테스트 그룹별 feature 브랜치
- M4 GREEN — Control + Boundary 통합: I-INT-* 통과
- M5 GUI: PyQt MainWindow
- M6 Golden Master + REFACTOR

각 M2~M6는 별도 feature 브랜치 + A2 PR (02 §2.3).

---

## 9. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — Test Plan + RED Skeleton 방식 결정 |

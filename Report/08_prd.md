# PRD — Magic Square 4×4 (Partial Solver) — Solver 도메인 정식 PRD

> 작성일: 2026-05-29
> 단계: P-02 PRD (Gherkin 포함) — 워크북 L2596~3315 산출물
> 상태: Active v1.0 (`Report/03_prd.md` v1.0 SUPERSEDED을 대체)
> 전제 문서:
> - [`01_problem_definition.md`](./01_problem_definition.md) v2.0 — Solver 문제 정의, I1~I12
> - [`02_branching_strategy.md`](./02_branching_strategy.md) §2.3 — PR 카덴스
> - [`04_architecture_design.md`](./04_architecture_design.md) — ECB 4계층 + Traceability
> - [`05_cursor_rules_design.md`](./05_cursor_rules_design.md) + `.cursorrules`
> - [`07_skills_agents_user_journey_compressed.md`](./07_skills_agents_user_journey_compressed.md) — Epic·Persona·Story 3

---

## 1. 개요 (Overview)

**Magic Square 4×4 (Partial Solver)** 는 빈칸 2개가 있는 4×4 정수 행렬을 입력으로 받아, 누락된 두 수를 찾아 마방진을 완성한 결과를 `int[6] = [r1,c1,n1,r2,c2,n2]` (1-index, row-major 빈칸 순서) 형식으로 반환하는 시스템이다.

알고리즘 규약: **Step A** (작은 수→첫 빈칸, 큰 수→둘째 빈칸) 우선 → 실패 시 **Step B** (reverse) → 둘 다 실패 시 **`NO_VALID_MAGIC_SQUARE`** 정의된 실패.

본 시스템의 본질은 "마방진을 푸는 알고리즘"이 아니라 **invariant-first 사고 훈련용 학습 도구**이다 (07 §5 Epic).

---

## 2. 목표 / 비목표

### 2.1 Goals (Success Criteria)

| ID | 목표 | 측정 |
| --- | --- | --- |
| G1 | invariant I1~I12를 결정론적으로 검증·강제 | 04 §4.5 12행 Traceability 모두 테스트 ID 매핑 |
| G2 | 입력 검증 실패와 도메인 실패를 분리된 에러 코드(E001~E004 vs E005)로 응답 | §6.2 에러 코드 표 |
| G3 | 모든 production 코드는 RED → GREEN 순서로만 작성 (M1) | git history 검증 |
| G4 | PyQt GUI로 부분 마방진 입력 → 풀기 → 결과 표시 작동 | §9 GUI 절 검증 절차 |
| G5 | Golden Master 회귀 테스트로 출력 형식 변경 시 즉시 fail | §11 §I-GM-01 |

### 2.2 Non-goals

| ID | 비목표 | 사유 |
| --- | --- | --- |
| NG1 | N×N (N≠4) 마방진 | 01 §1.2 학습 균형점 |
| NG2 | 마방진 자동 생성 (빈칸 16개) | 본 프로젝트는 Solver이지 Generator가 아님 |
| NG3 | 빈칸 ≠ 2 인 입력 | 01 §1.1 본 도메인 정의 |
| NG4 | 회전·반사 동치류 분류 | Post-MVP |
| NG5 | 웹/모바일 GUI | PyQt 데스크톱만 |
| NG6 | 다국어 | 한국어 + 영어 코드명 |

---

## 3. 타깃 사용자 (07 §6 재인용)

- **P1 (우선)**: TDD를 학습하는 개발자 — 로컬 터미널 + GUI 사용
- **P2 (부차)**: 마방진을 배우는 학습자 — GUI 중심

충돌 시 P1 우선. (07 §6 참조)

---

## 4. 입력 계약 (01 §5.3 I1~I4 정합)

```
grid: List[List[int]]
  - shape: 4×4 (행 4개, 각 행 길이 4)              # I1
  - 빈칸(0) 개수: 정확히 2                           # I2
  - 모든 값 ∈ {0} ∪ {1, 2, ..., 16}                # I3
  - 0이 아닌 값은 중복되지 않음                       # I4
```

위반 시 Boundary 단에서 `INPUT_ERROR` 분류로 반환, Domain 호출 0회 (I12).

---

## 5. 출력 계약 (01 §5.3 I7·I8·I9·I10 정합)

### 5.1 성공 출력

```
result: List[int] of length 6
  = [r1, c1, n1, r2, c2, n2]
  - r1,r2,c1,c2 ∈ [1, 4]                          # I10 (1-index)
  - n1,n2 ∈ [1, 16] (누락 두 수)
  - (r1,c1) ≺ (r2,c2) (row-major 빈칸 순서)        # I7
  - Step A 성공이면 n1 < n2                        # I8
  - Step A 실패·Step B 성공이면 n1 > n2 (reverse)  # I9
```

### 5.2 실패 출력 (도메인)

`E005 NO_VALID_MAGIC_SQUARE` (Step A·B 모두 실패, I11)

---

## 6. 기능 요구사항 (Functional Requirements) + Gherkin AC

### FR-01 InputValidator (Boundary)

**책임**: I1~I4 검증. 위반 시 정의된 입력 에러를 반환, Domain 호출 차단(I12).

#### AC-FR-01-01 (4×4 아닌 입력)

```gherkin
Feature: InputValidator는 4x4가 아닌 행렬을 거부한다 (I1)

Scenario: 3x4 행렬 입력
  Given grid는 3행 4열의 정수 행렬이다
  When InputValidator.validate(grid)를 호출하면
  Then 결과는 error이고 code는 "E001 INVALID_SIZE"이며
  And  message는 "Grid must be 4x4."이고
  And  Domain Service는 호출되지 않는다 (call_count == 0)

Scenario: None 입력
  Given grid는 None이다
  When InputValidator.validate(grid)를 호출하면
  Then 결과는 error이고 code는 "E001 INVALID_SIZE"
  And  Domain Service 호출 0회

Scenario: 빈 리스트 입력
  Given grid는 []
  When validate
  Then E001 INVALID_SIZE, Domain 호출 0회

Scenario: 5x5 행렬
  Given grid는 5행 5열
  When validate
  Then E001 INVALID_SIZE, Domain 호출 0회
```

테스트 ID 매핑: `U-VAL-01`~`U-VAL-05`, `U-FLOW-02`

#### AC-FR-01-02 (빈칸 개수)

```gherkin
Feature: InputValidator는 빈칸이 정확히 2개가 아니면 거부한다 (I2)

Scenario: 빈칸 0개
  Given grid는 4x4이며 0이 없다
  When validate
  Then E002 INVALID_BLANK_COUNT, message="Grid must contain exactly 2 blank cells (0)."
  And  Domain 호출 0회

Scenario: 빈칸 1개
  Given grid는 4x4이며 0이 1개
  When validate
  Then E002 INVALID_BLANK_COUNT, Domain 호출 0회

Scenario: 빈칸 3개
  Given grid는 4x4이며 0이 3개
  When validate
  Then E002 INVALID_BLANK_COUNT, Domain 호출 0회
```

테스트 ID 매핑: `U-VAL-06`~`U-VAL-08`

#### AC-FR-01-03 (값 범위)

```gherkin
Feature: 값은 {0} ∪ {1..16} 범위여야 한다 (I3)

Scenario: -1 포함
  Given grid는 4x4, 값 중 -1이 존재
  When validate
  Then E003 INVALID_VALUE_RANGE, message="All values must be in [0, 16]."

Scenario: 17 포함
  Given grid는 4x4, 값 중 17이 존재
  When validate
  Then E003 INVALID_VALUE_RANGE
```

테스트 ID 매핑: `U-VAL-09`, `U-VAL-10`

#### AC-FR-01-04 (0 제외 중복 금지)

```gherkin
Feature: 0이 아닌 값은 중복될 수 없다 (I4)

Scenario: 5가 두 번
  Given grid는 4x4, 1~16 + 0 두 개를 포함하되 5가 두 번 등장
  When validate
  Then E004 DUPLICATE_VALUE, message="Non-zero values must be unique."
```

테스트 ID 매핑: `U-VAL-11`

### FR-02 BlankFinder (Domain)

**책임**: 빈칸 좌표를 row-major 순서로 반환 (I7).

```gherkin
Feature: BlankFinder는 빈칸 2개를 row-major 순서로 반환한다

Scenario: (1,1)과 (2,3)이 빈칸
  Given grid는 4x4, 빈칸 위치 (1,1)·(2,3) (1-index)
  When BlankFinder.find(grid)를 호출하면
  Then 결과는 [Coordinate(1,1), Coordinate(2,3)] 순서다
```

테스트 ID: `D-LOC-01`~`D-LOC-03`

### FR-03 MissingNumberFinder (Domain)

**책임**: {1..16} − grid에 등장한 값 = 누락 두 수. 작은 수 먼저 정렬 (I8 전제).

```gherkin
Feature: MissingNumberFinder는 누락된 두 수를 정렬해 반환한다

Scenario: 7과 12가 누락
  Given grid는 0이 아닌 14개 값 + 0 두 개를 가지며 {1..16} − 14개 = {7, 12}
  When MissingNumberFinder.find(grid)
  Then MissingPair(n_small=7, n_big=12)
```

테스트 ID: `D-MISS-01`~`D-MISS-03`

### FR-04 MagicSquareValidator (Domain)

**책임**: 완성된 격자가 마방진인지 판정 (I5·I6).

```gherkin
Feature: MagicSquareValidator는 행/열/대각선 합이 모두 MAGIC_CONSTANT일 때만 True

Scenario: 알려진 마방진
  Given grid는 [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
  When MagicSquareValidator.is_magic(grid)
  Then 결과는 True

Scenario: 한 행 합 위반
  Given grid는 위 마방진에서 첫 행의 16과 13을 바꾼 격자
  When is_magic
  Then 결과는 False
```

테스트 ID: `D-VAL-01`~`D-VAL-07`

> 본 FR이 사용하는 상수: `MAGIC_CONSTANT = 34`, `GRID_SIZE = 4`. **SSOT — 리터럴 4·34 직접 사용 금지 (.cursorrules forbidden)**.

### FR-05 SolutionAttempter (Domain)

**책임**: (격자, 빈칸 쌍, (n_a, n_b)) → 새 격자. 순수 함수, 불변.

테스트 ID: `D-ATT-01`, `D-ATT-02`

### FR-06 StepABSolver (Domain — 오케스트레이션)

**책임**: I8·I9·I11 — Step A → 실패 시 Step B → 둘 다 실패 시 `NoValidMagicSquareError`.

```gherkin
Feature: StepABSolver는 Step A 우선, 실패 시 reverse, 둘 다 실패 시 정의된 실패

Scenario: Step A 성공
  Given 검증 통과한 grid, 누락 (7, 12)
  And   배치 (7→첫 빈칸, 12→둘째 빈칸) 결과가 마방진이다
  When StepABSolver.solve(grid)
  Then 결과는 [r1,c1,7,r2,c2,12] (r1,c1과 r2,c2는 row-major 빈칸 좌표)

Scenario: Step A 실패, Step B (reverse) 성공
  Given 검증 통과한 grid, 누락 (7, 12)
  And   Step A 결과는 마방진 아님
  And   Step B (12→첫, 7→둘째) 결과가 마방진이다
  When solve
  Then 결과는 [r1,c1,12,r2,c2,7]

Scenario: Step A·B 모두 실패
  Given 검증 통과한 grid, 누락 두 수
  And   Step A·B 어느 결과도 마방진이 아니다
  When solve
  Then NoValidMagicSquareError 발생 (Boundary가 E005 NO_VALID_MAGIC_SQUARE로 변환)
```

테스트 ID: `D-SOL-01`~`D-SOL-06`

### FR-07 SolvePartialMagicSquare (Control — Use Case)

**책임**: Boundary 검증 후 호출되어 Domain 오케스트레이션 위임.

테스트 ID: `tests/control/test_solve_partial_magic_square.py` (단위 + I-INT)

### FR-08 SolveBoundary (Boundary)

**책임**: 외부 호출자(GUI 또는 라이브러리)에게 통합 진입점 제공. InputValidator 호출 → 성공 시 Control 호출 → Domain 결과를 int[6] 또는 ErrorObject로 변환.

테스트 ID: `U-OUT-01`~`U-OUT-03`, `U-FLOW-01`, `U-FLOW-02`

### FR-09 PyQt GUI MainWindow (Boundary, GUI)

**책임**: 워크북 L4841~5024 정합.

- 창 제목: `"Magic Square 4x4"`
- 4×4 QSpinBox 격자 (값 0~16)
- "풀기" 버튼 → SolveBoundary.solve(grid) 호출
- 결과 표시 영역: 성공 시 int[6] + 채워진 격자 시각화, 실패 시 에러 코드·메시지

테스트는 통합 단계 + 수동 시각 검증.

---

## 7. 비기능 요구사항 (NFR)

| ID | 분류 | 요구사항 |
| --- | --- | --- |
| NFR-1 | 결정성 | 모든 Domain Service는 순수 함수 — 전역 상태·시간·랜덤 의존 금지 |
| NFR-2 | 성능 | 단일 격자 solve <10ms (4×4 규모 자명) |
| NFR-3 | 신뢰성 | 모든 production 코드는 직전 RED 결과로만 (M1) |
| NFR-4 | 가독성 | identifier ↔ invariant ID(I*) 시각적 매핑 |
| NFR-5 | 의존성 | runtime: 표준 라이브러리 + PyQt5/6 (GUI만). dev: pytest |
| NFR-6 | 호환성 | Python ≥ 3.10 |
| NFR-7 | 메시지 | 에러 메시지는 §6의 각 AC에 명시된 문구 그대로 (문자 단위 동등). 한국어 메시지는 PRD v2에서 검토 |
| NFR-8 | 에러/실패 분리 | INPUT_ERROR(E001~E004) vs DOMAIN_FAILURE(E005) 별도 채널 |

---

## 8. 에러 코드 (정문구 SSOT)

| Code | Type | Message (정확한 문구) | 위반 invariant | 테스트 ID |
| --- | --- | --- | --- | --- |
| E001 | INPUT_ERROR | `Grid must be 4x4.` | I1 | U-VAL-01~05 |
| E002 | INPUT_ERROR | `Grid must contain exactly 2 blank cells (0).` | I2 | U-VAL-06~08 |
| E003 | INPUT_ERROR | `All values must be in [0, 16].` | I3 | U-VAL-09~10 |
| E004 | INPUT_ERROR | `Non-zero values must be unique.` | I4 | U-VAL-11 |
| E005 | DOMAIN_FAILURE | `No valid magic square found.` | I11 | D-SOL-03, U-OUT-02, I-INT-07 |

> 본 표는 .cursorrules `forbidden.alternative` 와 코드 내 상수 모듈(`src/boundary/error_codes.py`)의 SSOT. 테스트는 message 문자 단위 동등 비교.

---

## 9. CLI / GUI 인터페이스

### 9.1 CLI (라이브러리 + 간단 호출 진입점)

```
python -m boundary.solve_boundary --file grid.json
```

입력 파일 예시(grid.json):
```json
{"grid": [[0,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,0]]}
```

출력:
- 성공: `{"ok": true, "result": [1,1,16,4,4,1]}`
- 실패: `{"ok": false, "error": {"code":"E005", "type":"DOMAIN_FAILURE", "message":"No valid magic square found."}}`

종료 코드: 0=성공, 1=DOMAIN_FAILURE, 2=INPUT_ERROR

### 9.2 GUI (PyQt — 워크북 L4987~5024 정합)

```
+------------------------- Magic Square 4x4 -------------------------+
|                                                                    |
|  [ SpinBox ][ SpinBox ][ SpinBox ][ SpinBox ]                      |
|  [ SpinBox ][ SpinBox ][ SpinBox ][ SpinBox ]                      |
|  [ SpinBox ][ SpinBox ][ SpinBox ][ SpinBox ]                      |
|  [ SpinBox ][ SpinBox ][ SpinBox ][ SpinBox ]                      |
|                                                                    |
|              [   풀기   ]                                          |
|                                                                    |
|  결과:                                                              |
|    ┌────────────────────────────────────┐                          |
|    │ [r1,c1,n1,r2,c2,n2] = [1,1,16,4,4,1] │                       |
|    │ 완성된 격자:                          │                        |
|    │   16  3  2 13                        │                        |
|    │    5 10 11  8                        │                        |
|    │    9  6  7 12                        │                        |
|    │    4 15 14  1                        │                        |
|    └────────────────────────────────────┘                          |
+--------------------------------------------------------------------+
```

- 각 SpinBox: range 0~16, default 0
- "풀기" 클릭 → SolveBoundary.solve(grid) 호출
- 성공: int[6] 표시 + 완성 격자 표시
- 실패: 에러 코드/메시지를 그대로 표시 (E001~E005)
- 의존성 주입: UIBoundary는 `SolvePartialMagicSquare` (Control)을 생성자로 주입받음 (app.py composition root)

---

## 10. 범위 (MVP)

### MVP에 포함

- FR-01~FR-08 (코어 + Boundary + Control + Domain 전체)
- 정상·실패 출력 양쪽
- E001~E005 에러 코드 + 정확한 메시지
- PyQt GUI MainWindow (FR-09)
- Golden Master 1건 (§11 I-GM-01)

### Post-MVP

- 회전·반사 동치 (NG4)
- 다국어 (NG6)
- File Repository 구현 (Data Layer — Golden Master 단계에서 도입)

---

## 11. 회귀 보호 (Lock List — 04 §4.3 정합)

| Lock | 잠금 대상 | 잠금 테스트 |
| --- | --- | --- |
| L1 | int[6] 구조 | U-OUT-01, D-SOL-04~05 |
| L2 | 1-index | U-OUT-03, D-SOL-04 |
| L3 | E001~E005 코드 식별자 | U-VAL-*, U-OUT-02 |
| L4 | 에러 메시지 문구 (§8) | U-MSG-* (Test Plan에서 정의) |
| L5 | MAGIC_CONSTANT=34, GRID_SIZE=4 | D-VAL-07 (정적), D-VAL-01 |
| L6 | Domain 호출 0회 (invalid 시) | U-FLOW-02, I-INT-03~06 |
| L7 (NEW) | Golden Master baseline | I-GM-01 |

### Golden Master I-GM-01

- baseline: 사전 합의된 N=10건의 정상 입력 → 기대 int[6] 매핑
- 매 머지마다 baseline 매칭 확인. 변경 시 명시적 승인 + baseline 갱신 PR

---

## 12. 커버리지 임계 (04 §4.4 재인용)

| 계층 | Line | Branch |
| --- | --- | --- |
| Domain | ≥ 95% | ≥ 90% |
| Boundary | ≥ 85% | ≥ 80% |
| Data | ≥ 80% | ≥ 70% |
| Control | ≥ 90% | ≥ 85% |

CI 미달 시 빌드 실패. PR 본문에서 명시적 승인 없이 임계 하향 금지.

---

## 13. Traceability (04 §4.5 + 본 PRD FR 매핑)

| Invariant | PRD FR | AC | 테스트 ID | 컴포넌트 |
| --- | --- | --- | --- | --- |
| I1 | FR-01 | AC-FR-01-01 | U-VAL-01~05 | InputValidator |
| I2 | FR-01 | AC-FR-01-02 | U-VAL-06~08 | InputValidator |
| I3 | FR-01 | AC-FR-01-03 | U-VAL-09~10 | InputValidator |
| I4 | FR-01 | AC-FR-01-04 | U-VAL-11 | InputValidator |
| I5 | FR-04 | (정적) | D-VAL-07 | MagicConstant VO |
| I6 | FR-04 | FR-04 AC | D-VAL-01~06 | MagicSquareValidator |
| I7 | FR-02 | FR-02 AC | D-LOC-01~03, D-SOL-06 | BlankFinder |
| I8 | FR-06 | FR-06 Step A | D-SOL-01, I-INT-01 | StepABSolver |
| I9 | FR-06 | FR-06 Step B | D-SOL-02, I-INT-02 | StepABSolver |
| I10 | FR-08 | §5.1 | U-OUT-01, U-OUT-03, D-SOL-04~05 | Boundary + Domain |
| I11 | FR-06 | FR-06 둘 다 실패 | D-SOL-03, U-OUT-02, I-INT-07 | StepABSolver + Boundary |
| I12 | FR-01 | 모든 AC-FR-01-* | U-FLOW-02, I-INT-03~06 | InputValidator |

---

## 14. 마일스톤

| M | 이름 | 산출 | DoD |
| --- | --- | --- | --- |
| M0 | PRD 정착 | `Report/08_prd.md` | 본 문서 머지 |
| M1 | Test Plan + RED Skeleton | `tests/**/test_*.py` (모든 RED, 의도된 fail만) | pytest 수집 OK, 모든 테스트 fail 또는 ImportError로 RED |
| M2 | GREEN — InputValidator | `src/boundary/input_validator.py` | U-VAL-01~11, U-FLOW-02 GREEN |
| M3 | GREEN — Domain Services | `src/entity/*.py` (FR-02~FR-06) | D-LOC, D-MISS, D-VAL, D-ATT, D-SOL 모두 GREEN |
| M4 | GREEN — Control + Boundary 통합 | `src/control/*.py`, `src/boundary/solve_boundary.py` | I-INT-01~07 GREEN |
| M5 | GUI MainWindow | `src/boundary/screen/app.py` | GUI 띄움 + 부분 마방진 입력 → 풀기 → 결과 표시 |
| M6 | Golden Master + Refactor | baseline + refactor 사이클 | I-GM-01 GREEN, refactor 후 전체 테스트 동일 |

> M0 머지 후 다음 작업은 M1 (Test Plan + RED Skeleton). `feature/red-skeleton` 브랜치 + A1 PR.

---

## 15. 본 PRD가 결정하지 않는 것 (의도적 보류)

- Repository File 구현체의 직렬화 포맷 (JSON vs CSV) — Golden Master 단계에서
- PyQt 5 vs 6 선택 — GUI 구현 시점 (환경에 맞춰)
- 회전·반사 동치 처리 — Post-MVP
- CI/CD 도입 — 별도 마일스톤

---

## 16. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — Solver 도메인, Gherkin AC 포함, 03 PRD v1.0 (Judge) 대체 |

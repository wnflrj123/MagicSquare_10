# 4×4 Magic Square — 아키텍처·테스트·통합 설계 보고서

> 작성일: 2026-05-29
> 작성 단계: 아키텍처 설계(Architecture Design) — 워크북 §과제 1 "아키텍처/테스트/통합 요청"의 산출물
> 전제 문서:
> - [`01_problem_definition.md`](./01_problem_definition.md) v2.0 — Solver 도메인 정의, invariant I1~I12
> - [`02_branching_strategy.md`](./02_branching_strategy.md) — RGR 정합 브랜치 전략
> - `03_prd.md` — ⚠️ SUPERSEDED (참조 금지)
> 본 문서가 결정하는 것: **Logic / Screen / Data / Integration 4계층의 책임 분리, 도메인 API 시그니처, 테스트 설계(RED 우선), Traceability Matrix**
> 본 문서가 결정하지 않는 것: 구현 코드, 자료구조의 내부 표현, PRD(P-02 단계 산출), CLI/Web UI 형태

---

## 0. 본 보고서의 약속

- **구현 코드 0줄.** 시그니처·계약·테스트 ID·체크리스트만 다룬다.
- **모든 규칙은 검증 가능(verifiable)** 하다 — "적절히/충분히" 같은 모호 표현 금지.
- **테스트 ID 체계**:
  - `D-*` Domain 단위 테스트 (Logic Layer)
  - `U-*` UI/Boundary 단위 테스트 (Screen Layer)
  - `DAT-*` Data Layer 단위 테스트
  - `I-INT-*` Integration 테스트
- **에러 코드 체계**: `E001~E005` (본 문서 §2.2에서 정의, 추후 PRD에서 메시지 문구 확정)
- **명명된 상수(SSOT)**: `GRID_SIZE=4`, `BLANK_VALUE=0`, `MIN_VALUE=1`, `MAX_VALUE=16`, `MAGIC_CONSTANT=34`, `BLANK_COUNT=2`, `OUTPUT_LENGTH=6`. 코드에 리터럴 4·34 등장 금지.

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념 (Entities / Value Objects / Domain Services + SRP)

### Value Objects (불변, 비교 가능)

| 이름 | 역할 (단일 책임) |
| --- | --- |
| `MagicConstant` | 4×4의 행/열/대각선 합 목표값 = 34. SSOT. 외부에서 임의 변경 불가 |
| `GridSize` | 격자 변 길이 = 4. SSOT |
| `Coordinate` | (row, col) 한 칸의 위치. **1-index** (1≤r,c≤4) |
| `BlankCoordinates` | 두 개의 `Coordinate` 쌍. **row-major 순서로 정렬됨** (불변식) |
| `MissingPair` | 두 개의 누락된 수 (n_small, n_big) where n_small < n_big |
| `SolutionResult` | 최종 출력 = `int[6] = [r1, c1, n1, r2, c2, n2]` (1-index) |

### Entities (식별성·생명주기를 가진 도메인 객체)

| 이름 | 역할 |
| --- | --- |
| `MagicBoard` | 4×4 정수 행렬을 감싸는 도메인 객체. 값 읽기/특정 좌표에 값 배치(불변 복사 반환) 책임만 가진다. **입력 형식 검증은 책임이 아니다** (Boundary가 담당) |

### Domain Services (상태 없는 순수 로직)

| 이름 | 책임 (SRP) |
| --- | --- |
| `BlankFinder` | 격자 안의 빈칸(0) 좌표를 row-major 순서로 찾는다 |
| `MissingNumberFinder` | {1..16} − 격자에 존재하는 값들 = 누락된 두 수 (정렬해 `MissingPair`로 반환) |
| `MagicSquareValidator` | 주어진 격자가 마방진인지 판정 (I5·I6: 모든 행·열·대각선 합 = 34) |
| `SolutionAttempter` | (격자, 빈칸 좌표 쌍, 배치 순서) → 새 격자 생성. 마방진 판정은 호출자 책임 |
| `StepABSolver` | 위 4개를 오케스트레이션. Step A → 실패 시 Step B → 둘 다 실패 시 `NO_VALID_MAGIC_SQUARE` |

> **SRP 위반 체크**: `SolutionAttempter`는 "배치만" 한다. 판정은 하지 않는다. `MagicSquareValidator`는 "판정만" 한다. 배치하지 않는다. `StepABSolver`는 "순서만" 정한다. 판정·배치는 위임한다.

## 1.2 도메인 불변조건 (Invariants)

`01_problem_definition.md` v2.0 §5.3의 I1~I12 중 Domain Layer 책임 invariant:

| ID | Invariant | 검증 위치 |
| --- | --- | --- |
| I5 | `MAGIC_CONSTANT = 34` (4×4에서 1+..+16=136 → 136÷4=34) — SSOT, 리터럴 금지 | `MagicConstant` VO + 정적 분석 |
| I6 | 마방진 ⇔ 4개 행 합 = 4개 열 합 = 2개 대각선 합 = 34 (동시) | `MagicSquareValidator.is_magic` |
| I7 | 빈칸 좌표 순서 = row-major 스캔 순서 | `BlankFinder.find` |
| I8 | Step A 우선: (n_small → 첫 빈칸, n_big → 둘째 빈칸) | `StepABSolver.solve` |
| I9 | Step A 실패 시에만 Step B (reverse) 시도 | `StepABSolver.solve` |
| I10 | 출력은 `int[6] = [r1, c1, n1, r2, c2, n2]`, 1-index | `SolutionResult` VO + `StepABSolver.solve` 반환 |
| I11 | Step A·B 모두 실패 → `NO_VALID_MAGIC_SQUARE` 도메인 실패 | `StepABSolver.solve` |

> Domain은 I1~I4(입력 계약 검증)와 I12(invalid 입력 차단)를 **직접 책임지지 않는다** — Boundary 책임. 단, 잘못된 입력이 흘러들어왔을 때 방어적 어설션을 둘지는 §1.4에서 정의.

## 1.3 핵심 유스케이스 (도메인 관점)

| # | 유스케이스 | 책임 서비스 | 입력 | 출력 | 실패 |
| --- | --- | --- | --- | --- | --- |
| UC-D-1 | 빈칸 좌표 찾기 | `BlankFinder` | 4×4 격자 | `BlankCoordinates` (2개, row-major) | 빈칸 수 ≠ 2 (단, 도메인은 이를 가정함 — Boundary 책임) |
| UC-D-2 | 누락 수 찾기 | `MissingNumberFinder` | 4×4 격자 | `MissingPair` (n_small, n_big) | 동일 |
| UC-D-3 | 마방진 판정 | `MagicSquareValidator` | 4×4 격자 (완성) | `bool` | 없음 |
| UC-D-4 | 단일 배치 시도 | `SolutionAttempter` | 격자, `BlankCoordinates`, (n_first, n_second) | 새 4×4 격자 | 없음 |
| UC-D-5 | Step A → B 오케스트레이션 | `StepABSolver` | 4×4 격자 (빈칸 2) | `SolutionResult` (int[6]) | `NoValidMagicSquareError` |

## 1.4 Domain API — 내부 계약 (메서드 시그니처 수준, 코드 X)

> 시그니처 표기는 언어 중립 의도. Python 구현 시 type hint로, Java 구현 시 인터페이스로 변환.

| Service.Method | 입력 | 출력 | 실패 조건 |
| --- | --- | --- | --- |
| `BlankFinder.find(grid)` | `grid: Matrix[4][4]` | `list[Coordinate]` of length 2, row-major sorted | (도메인 가정: 빈칸 정확히 2개. 위반 시 `AssertionError` — 호출자 계약 위반) |
| `MissingNumberFinder.find(grid)` | `grid: Matrix[4][4]` | `MissingPair(n_small, n_big)`, n_small < n_big | (도메인 가정: 누락 수 정확히 2개) |
| `MagicSquareValidator.is_magic(grid)` | `grid: Matrix[4][4]` (완성) | `bool` | (입력에 0 포함 시 즉시 False — 미완성은 마방진 아님) |
| `SolutionAttempter.apply(grid, blanks, pair)` | `grid`, `blanks: BlankCoordinates`, `pair: (int, int)` | 새 `Matrix[4][4]` (입력 불변) | 없음 (순수 함수) |
| `StepABSolver.solve(grid)` | `grid: Matrix[4][4]` (빈칸 2) | `SolutionResult` (int[6]) | `NoValidMagicSquareError` (E005에 매핑) |

### Domain 측 도메인 예외

| 예외 | 발생 위치 | 매핑되는 Boundary 에러 코드 |
| --- | --- | --- |
| `NoValidMagicSquareError` | `StepABSolver.solve` | `E005 NO_VALID_MAGIC_SQUARE` |

> **방어적 어설션 정책**: Domain Service는 입력 계약(빈칸 2, 값 범위 등)을 **재검증하지 않는다.** Boundary가 보증한다고 가정한다. 단, 디버그 빌드/테스트 모드에서는 `assert` 로 가정을 확인할 수 있다. 운영 빌드에서는 가정 위반 시 `AssertionError` 전파 — 호출자 계약 위반은 정의된 도메인 실패가 아니다.

## 1.5 Domain 단위 테스트 설계 (RED 우선)

테스트는 모두 **RED 먼저** 작성. 구현은 RED를 통과시키는 최소 변경.

### D-LOC-* — BlankFinder

| Test ID | 케이스 | 입력 (요지) | 기대 출력 | 보호 invariant |
| --- | --- | --- | --- | --- |
| D-LOC-01 | 정상 — 빈칸 2개 row-major | 4×4, 빈칸 위치 (1,1)·(2,3) | `[(1,1), (2,3)]` | I7 |
| D-LOC-02 | 정상 — 빈칸이 끝줄·끝열 | (4,3)·(4,4) | `[(4,3), (4,4)]` | I7 |
| D-LOC-03 | 정상 — 빈칸 사이가 멀리 떨어짐 | (1,1)·(4,4) | `[(1,1), (4,4)]` | I7 |

### D-MISS-* — MissingNumberFinder

| Test ID | 케이스 | 입력 (요지) | 기대 출력 | 보호 invariant |
| --- | --- | --- | --- | --- |
| D-MISS-01 | 정상 — 누락 2개 정렬 반환 | {1..16} − {7, 12} 포함 | `MissingPair(7, 12)` | I8 (정렬 — small first) |
| D-MISS-02 | 정상 — 누락 1·2 같은 인접 | {1..16} − {1, 2} 포함 | `MissingPair(1, 2)` | I8 |
| D-MISS-03 | 정상 — 누락 1·16 양 끝 | {1..16} − {1, 16} 포함 | `MissingPair(1, 16)` | I8 |

### D-VAL-* — MagicSquareValidator

| Test ID | 케이스 | 입력 (요지) | 기대 출력 | 보호 invariant |
| --- | --- | --- | --- | --- |
| D-VAL-01 | 정상 마방진 → True | 알려진 4×4 마방진 1예시 | `True` | I5, I6 |
| D-VAL-02 | 행 합 위반 → False | 마방진에서 한 행 값 swap (다른 행과) | `False` | I6 |
| D-VAL-03 | 열 합 위반 → False | 마방진에서 두 열 사이 값 교환 | `False` | I6 |
| D-VAL-04 | 주대각선 합 위반 → False | 주대각선 한 칸을 다른 칸과 교환 (행·열은 유지) | `False` | I6 |
| D-VAL-05 | 부대각선 합 위반 → False | 부대각선 한 칸 교환 | `False` | I6 |
| D-VAL-06 | 0 포함 → False | 마방진에서 한 칸을 0으로 교체 | `False` | I6 (미완성은 마방진 아님) |
| D-VAL-07 | Magic Constant 리터럴 미사용 검증 | (정적 — grep으로 `34`/`4` 리터럴 0건) | — | I5 (SSOT) |

### D-ATT-* — SolutionAttempter

| Test ID | 케이스 | 기대 |
| --- | --- | --- |
| D-ATT-01 | 두 빈칸에 (n_a, n_b) 배치 → 새 격자에 정확한 위치에 값 배치 | 입력 격자 불변, 출력 격자만 변경 |
| D-ATT-02 | apply는 순수 함수 — 동일 입력 두 번 호출, 동일 출력 | 결정성 |

### D-SOL-* — StepABSolver (오케스트레이션)

| Test ID | 케이스 | 입력 시나리오 | 기대 출력 | 보호 invariant |
| --- | --- | --- | --- | --- |
| D-SOL-01 | Step A 성공 | 누락 (7, 12), Step A 배치(7→첫, 12→둘째)가 마방진 | `[r1,c1,7,r2,c2,12]` | I8 |
| D-SOL-02 | Step A 실패·Step B 성공 (reverse) | 누락 (7, 12), Step A 실패, Step B(12→첫, 7→둘째)가 마방진 | `[r1,c1,12,r2,c2,7]` | I9 |
| D-SOL-03 | Step A·B 모두 실패 | 어떤 조합도 마방진 안 됨 | `NoValidMagicSquareError` 발생 | I11 |
| D-SOL-04 | 출력 좌표는 1-index | 어떤 성공 케이스든 r,c ∈ [1,4] | (검증) | I10 |
| D-SOL-05 | 출력 길이 = 6 | 모든 성공 케이스 | `len == 6` | I10 |
| D-SOL-06 | 빈칸 순서가 row-major | 성공 시 첫 두 좌표 (r1,c1)가 row-major상 앞 | (검증) | I7 |

---

# 2) Screen Layer (UI Layer / Boundary) 설계

> 본 프로젝트에서 "UI"는 시각적 화면이 아니라 **외부 호출자와 도메인 사이의 경계(Boundary)** 다. CLI·라이브러리 함수·웹 API 어떤 형태든 본 §2의 계약을 만족해야 한다.

## 2.1 사용자/호출자 관점 시나리오

| # | 시나리오 | 흐름 |
| --- | --- | --- |
| S-1 | 정상 입력 → 정답 반환 | 호출자 → grid 전달 → Boundary 검증 통과 → Control 호출 → Domain → `int[6]` 반환 |
| S-2 | 정상 입력 → 도메인 실패 | 호출자 → grid 전달 → Boundary 검증 통과 → Control 호출 → Step A·B 실패 → `E005 NO_VALID_MAGIC_SQUARE` 반환 |
| S-3 | 입력 계약 위반 | 호출자 → 잘못된 grid 전달 → Boundary 검증 실패 → **Control·Domain 호출 0회** → `E001~E004` 반환 |

## 2.2 UI 계약 (Input / Output / Error Schema)

### Input Schema

```
grid: List[List[int]]   # 외부 표현은 언어별
  - 외형(shape) = 4×4 (행 4개, 각 행 길이 4)
  - 모든 셀의 값 ∈ {0} ∪ {1..16}
  - 0의 개수 = 정확히 2
  - 0이 아닌 값들은 모두 서로 다름 (중복 없음)
```

### Output Schema (성공)

```
result: List[int] of length 6
  = [r1, c1, n1, r2, c2, n2]
  - r1,r2,c1,c2 ∈ [1, 4]   # 1-index
  - n1,n2 ∈ [1, 16]        # 누락 두 수
  - (r1,c1) ≺ (r2,c2)      # row-major 순서
```

### Error Schema

```
error:
  type: "INPUT_ERROR" | "DOMAIN_FAILURE"
  code: enum  # 아래 표
  message: str  # 정확한 문구는 PRD에서 확정
```

| Code | Type | 의미 | 위반된 Invariant |
| --- | --- | --- | --- |
| E001 | INPUT_ERROR | `INVALID_SIZE` — 4×4가 아닌 입력 | I1 |
| E002 | INPUT_ERROR | `INVALID_BLANK_COUNT` — 빈칸 개수 ≠ 2 | I2 |
| E003 | INPUT_ERROR | `INVALID_VALUE_RANGE` — 값 ∉ {0}∪{1..16} | I3 |
| E004 | INPUT_ERROR | `DUPLICATE_VALUE` — 0 제외 중복 | I4 |
| E005 | DOMAIN_FAILURE | `NO_VALID_MAGIC_SQUARE` — Step A·B 모두 실패 | I11 |

> **에러와 실패의 분리** (01 §5.2 명시): `INPUT_ERROR`는 호출자의 계약 위반, `DOMAIN_FAILURE`는 입력은 합법이나 풀이가 존재하지 않음. 두 채널은 절대 섞이지 않는다.

## 2.3 UI 레벨 테스트 (Contract-first, RED 우선, Domain은 Mock)

Domain은 **mock/spy로 대체**하여 Boundary 단독 책임을 검증.

### U-VAL-* — 입력 검증

| Test ID | 입력 시나리오 | 기대 결과 | Domain 호출 횟수 |
| --- | --- | --- | --- |
| U-VAL-01 | grid = `None` | E001 INVALID_SIZE | 0 |
| U-VAL-02 | grid = 3×4 행렬 | E001 INVALID_SIZE | 0 |
| U-VAL-03 | grid = 4×3 행렬 | E001 INVALID_SIZE | 0 |
| U-VAL-04 | grid = 5×5 행렬 | E001 INVALID_SIZE | 0 |
| U-VAL-05 | grid = `[]` (빈) | E001 INVALID_SIZE | 0 |
| U-VAL-06 | grid = 4×4, 빈칸 0개 | E002 INVALID_BLANK_COUNT | 0 |
| U-VAL-07 | grid = 4×4, 빈칸 1개 | E002 INVALID_BLANK_COUNT | 0 |
| U-VAL-08 | grid = 4×4, 빈칸 3개 | E002 INVALID_BLANK_COUNT | 0 |
| U-VAL-09 | grid = 4×4, 값 -1 포함 | E003 INVALID_VALUE_RANGE | 0 |
| U-VAL-10 | grid = 4×4, 값 17 포함 | E003 INVALID_VALUE_RANGE | 0 |
| U-VAL-11 | grid = 4×4, non-zero 중복 (예: 5가 두 번) | E004 DUPLICATE_VALUE | 0 |

### U-FLOW-* — 흐름 보장 (Domain 호출 횟수)

| Test ID | 입력 | 기대 |
| --- | --- | --- |
| U-FLOW-01 | 유효한 4×4 | Domain Service `StepABSolver.solve` 호출 **정확히 1회** |
| U-FLOW-02 | 무효한 입력 (위 U-VAL-* 어느 케이스든) | Domain Service 호출 **정확히 0회** (mock spy `call_count == 0`) |

### U-OUT-* — 출력 계약

| Test ID | 시나리오 | 기대 |
| --- | --- | --- |
| U-OUT-01 | Domain mock이 `[1,1,7,2,3,12]` 반환 | Boundary 출력 = `[1,1,7,2,3,12]` (변형 없음), 길이 6 |
| U-OUT-02 | Domain mock이 `NoValidMagicSquareError` 발생 | Boundary 출력 = E005 NO_VALID_MAGIC_SQUARE 에러 객체 |
| U-OUT-03 | 좌표는 1-index 검증 | 출력의 r1,c1,r2,c2 ∈ [1,4] |

## 2.4 UX/출력 규칙 (에러 메시지 표준 — 문구 안)

> 정확한 문구는 P-02 단계 PRD에서 확정. 본 보고서는 **형식 규칙**만 못 박는다.

| 규칙 | 정의 |
| --- | --- |
| UX-R-1 | 모든 에러 메시지는 `<code>: <설명>` 형식 — 예: `E001: Grid must be 4x4.` |
| UX-R-2 | 메시지는 코드별로 **정확히 1개의 문구**만 가진다 (SSOT) — 테스트는 문자 단위 동등 비교 |
| UX-R-3 | 메시지에 **숫자 리터럴 직접 등장 금지** — `4`, `34` 등은 `GRID_SIZE`, `MAGIC_CONSTANT` 보간 |
| UX-R-4 | 성공 출력은 `int[6]` 그 자체 — 메시지 없음 |
| UX-R-5 | 에러 객체와 성공 객체는 **타입이 다르다** (호출자가 `isinstance`/`match`로 분기 가능) |

---

# 3) Data Layer 설계

## 3.1 목적 정의

본 프로젝트의 학습 가치는 알고리즘이 아니라 **계층 분리 + 계약 + 테스트**다. 따라서 Data Layer는:

- 실제 DB가 아니라 **저장/로드 인터페이스(Repository)** 만 정의한다.
- 구현은 메모리 또는 파일 — 교체 가능해야 한다.
- 사용 목적: (a) 입력 격자 보관 (재현성), (b) 결과 보관 (회귀 비교), (c) Golden Master 기반 자료 (워크북 후속 단계).

## 3.2 인터페이스 계약 (메서드 수준, 코드 X)

### `MatrixRepository` (Protocol/Interface)

| 메서드 | 입력 | 출력 | 실패 |
| --- | --- | --- | --- |
| `save_input(id, grid)` | `id: str`, `grid: Matrix[4][4]` | `None` | `DUPLICATE_ID` (이미 존재) |
| `load_input(id)` | `id: str` | `Matrix[4][4]` | `NOT_FOUND` |
| `save_result(id, result)` | `id: str`, `result: int[6]` | `None` | `DUPLICATE_ID` |
| `load_result(id)` | `id: str` | `int[6]` | `NOT_FOUND` |
| `exists(id)` | `id: str` | `bool` | 없음 |
| `list_ids()` | — | `list[str]` | 없음 |

> Data Layer의 에러는 Boundary 에러 코드(E001~E005)와 **다른 네임스페이스**를 가진다 — 예: `DAT-E001 NOT_FOUND`, `DAT-E002 DUPLICATE_ID`, `DAT-E003 CORRUPT_DATA`. 두 네임스페이스가 섞이면 호출자가 혼란.

## 3.3 구현 옵션 비교 — InMemory vs File

| 항목 | (A) InMemory | (B) File (JSON) |
| --- | --- | --- |
| 영속성 | 프로세스 종료 시 소실 | 디스크에 영구 보존 |
| 의존성 | 표준 라이브러리만 | 표준 라이브러리 (`json`, `os`) |
| 테스트 격리 | 자동 (인스턴스마다 새 dict) | 임시 디렉터리 fixture 필요 |
| 동시성 | 단일 프로세스만 | 다중 프로세스 시 락 필요 (MVP 범위 외) |
| Golden Master 호환 | ❌ (재시작 시 소실) | ✅ (파일이 baseline 자체) |
| 학습 가치 | 인터페이스/책임 분리 체험 | 직렬화·계약·실패 복구 체험 |

**추천**: **A → B 순차 진행**.

1. MVP는 `(A) InMemory` 1개 구현으로 시작 — Repository 인터페이스 + Domain·Boundary가 인터페이스만 의존하는지 확인.
2. Golden Master 단계에서 `(B) File` 구현 추가 — 동일 인터페이스 테스트(LSP 검증)로 두 구현이 호환임을 확인.

## 3.4 Data 레이어 테스트

### DAT-MEM-* (InMemory 구현)

| Test ID | 케이스 | 기대 |
| --- | --- | --- |
| DAT-MEM-01 | save → load 왕복 동일성 | 저장한 grid와 load 결과가 동일 |
| DAT-MEM-02 | load 미존재 id | `NOT_FOUND` 발생 |
| DAT-MEM-03 | save 중복 id | `DUPLICATE_ID` 발생 |
| DAT-MEM-04 | 저장된 4×4 격자의 shape 보존 | row=4, col=4 |
| DAT-MEM-05 | exists는 save 전후 정확한 bool | `False` → save → `True` |

### DAT-FILE-* (File 구현 — Golden Master 단계 후 추가)

| Test ID | 케이스 | 기대 |
| --- | --- | --- |
| DAT-FILE-01 | save → load 왕복 동일성 | 동일 |
| DAT-FILE-02 | 미존재 파일 load | `NOT_FOUND` |
| DAT-FILE-03 | 손상된 JSON load | `CORRUPT_DATA` |
| DAT-FILE-04 | 파일 시스템 권한 없음 (write fail) | 도메인 중립 IO 오류로 전파 |

### DAT-CONTRACT-* (구현 무관 — Repository 계약 자체)

| Test ID | 케이스 | 적용 대상 |
| --- | --- | --- |
| DAT-CONTRACT-01 | 모든 Repository 구현은 save→load 왕복 동일성 만족 | InMemory + File |
| DAT-CONTRACT-02 | 모든 구현은 NOT_FOUND를 동일 예외로 발생 | InMemory + File |

> **LSP (Liskov Substitution Principle)**: DAT-CONTRACT-* 는 parametrize로 모든 구현에 동일 적용. 한 구현만 깨도 회귀로 즉시 발견.

---

# 4) Integration & Verification

## 4.1 통합 경로 정의

### 의존성 방향 (Clean Architecture)

```
[Boundary (UI/Adapter)]
        │ depends on (interface)
        ▼
[Control (Use Case Orchestration)]
        │ depends on (interfaces)
        ▼
[Domain Services + Repository Interface]
        │
        └─ Domain ← no external dependencies
           Repository Interface ← implemented by Data Layer
                                       ▲
                                       │ implements
                                  [Data Layer (InMemory/File)]
```

규칙:
- **Domain은 외부 의존성 0개** (표준 라이브러리만)
- **Data Layer는 Repository 인터페이스만 안다** (Domain Service 호출 금지)
- **Boundary는 Control 인터페이스만 안다** (Domain Service 직접 호출 금지)
- **Control은 Domain Service + Repository 인터페이스를 안다** (Data 구현체는 모름)

### 호출 흐름 (정상 케이스)

```
호출자
  │
  ▼
Boundary.solve(grid)
  │  1. 입력 계약 검증 (I1~I4)
  │  2. 검증 통과 시:
  ▼
Control.execute(grid)               ← Use Case
  │  3. (선택) Repository.save_input(...)
  │  4. Domain Service 오케스트레이션:
  ▼
   StepABSolver.solve(grid)
     │  4-1. BlankFinder.find(grid) → blanks
     │  4-2. MissingNumberFinder.find(grid) → pair
     │  4-3. SolutionAttempter.apply(...) Step A
     │  4-4. MagicSquareValidator.is_magic(...) — Step A 검증
     │  4-5. Step A 실패 시: apply Step B + validate
     ▼
   → int[6] or NoValidMagicSquareError
  │
  ▼
Boundary.solve 결과 변환 (성공: int[6] / 실패: E005)
  │
  ▼
호출자
```

## 4.2 통합 테스트 시나리오

### 정상 (≥ 2건)

| Test ID | 시나리오 | 기대 |
| --- | --- | --- |
| I-INT-01 | 유효 입력 + Step A 성공 | `int[6]`, n1 < n2 순서 |
| I-INT-02 | 유효 입력 + Step A 실패·Step B 성공 (reverse success) | `int[6]`, n1 > n2 순서 |

### 실패 (≥ 3건)

| Test ID | 시나리오 | 기대 | Domain 호출 |
| --- | --- | --- | --- |
| I-INT-03 | 4×4 아닌 입력 | E001 INVALID_SIZE | 0회 |
| I-INT-04 | 빈칸 ≠ 2 | E002 INVALID_BLANK_COUNT | 0회 |
| I-INT-05 | 값 범위 위반 | E003 INVALID_VALUE_RANGE | 0회 |
| I-INT-06 | 0 제외 중복 | E004 DUPLICATE_VALUE | 0회 |
| I-INT-07 | 유효 입력 + Step A·B 둘 다 실패 | E005 NO_VALID_MAGIC_SQUARE | 1회 |

### 통합 회귀 (Golden Master 단계 진입 후)

| Test ID | 시나리오 |
| --- | --- |
| I-GM-01 | 사전 합의된 입력 N건에 대해 출력이 baseline 파일과 정확히 일치 |

## 4.3 회귀 보호 규칙

### 변경 금지 (계약/출력 포맷)

다음은 **머지 시 변경되면 빌드 실패** 하도록 테스트로 잠근다:

| # | 잠금 대상 | 잠금 테스트 |
| --- | --- | --- |
| L1 | 출력 형식 `int[6]` 구조 | U-OUT-01, D-SOL-04~05 |
| L2 | 좌표는 1-index | U-OUT-03, D-SOL-04 |
| L3 | 에러 코드 식별자 (E001~E005) | U-VAL-*, U-OUT-02 |
| L4 | 에러 메시지 문구 (PRD 확정 후) | U-MSG-* (P-02 후 추가) |
| L5 | Magic Constant = 34 | D-VAL-07 (정적), D-VAL-01 |
| L6 | invalid 입력 시 Domain 호출 0회 | U-FLOW-02, I-INT-03~06 |

### 기존 테스트 유지 정책

- **테스트 삭제 PR은 별도 리뷰** — 기능 제거가 명시되지 않으면 머지 거부.
- **테스트 약화 금지** — 예: assert 강도를 낮추거나 `pytest.skip` 추가는 사유서 필수.
- **RED → GREEN 순서 보존** — 02 §2.1 main 머지 정책과 결합.

## 4.4 커버리지 목표 (정확한 수치)

| 계층 | 라인 커버리지 | 분기 커버리지 | 측정 방법 |
| --- | --- | --- | --- |
| Domain Logic | ≥ **95%** | ≥ 90% | `pytest --cov=src/domain` |
| UI Boundary | ≥ **85%** | ≥ 80% | `pytest --cov=src/boundary` |
| Data Layer | ≥ **80%** | ≥ 70% | `pytest --cov=src/data` |
| Control (orchestration) | ≥ 90% | ≥ 85% | `pytest --cov=src/control` |

> 커버리지 임계 미달 시 CI 실패. 임계는 PR 본문에서 명시적 동의 없이 낮출 수 없다.

## 4.5 Traceability Matrix (필수)

| Invariant | 도메인 규칙 | 유스케이스 | 계약 (Contract) | 테스트 ID | 담당 컴포넌트 |
| --- | --- | --- | --- | --- | --- |
| I1 | 입력 = 4×4 | 입력 검증 | E001 INVALID_SIZE | U-VAL-01~05, I-INT-03 | Boundary `InputValidator` |
| I2 | 빈칸 = 정확히 2 | 입력 검증 | E002 INVALID_BLANK_COUNT | U-VAL-06~08, I-INT-04 | Boundary `InputValidator` |
| I3 | 값 ∈ {0}∪{1..16} | 입력 검증 | E003 INVALID_VALUE_RANGE | U-VAL-09~10, I-INT-05 | Boundary `InputValidator` |
| I4 | 0 제외 중복 금지 | 입력 검증 | E004 DUPLICATE_VALUE | U-VAL-11, I-INT-06 | Boundary `InputValidator` |
| I5 | `MAGIC_CONSTANT = 34` SSOT | 마방진 판정 기반 | (상수) | D-VAL-01, D-VAL-07 (정적) | Domain VO `MagicConstant` |
| I6 | 행/열/대각선 합 = 34 동시 | 마방진 판정 | `is_magic` → bool | D-VAL-01~06 | Domain `MagicSquareValidator` |
| I7 | 빈칸 순서 = row-major | 빈칸 찾기 | `BlankCoordinates` | D-LOC-01~03, D-SOL-06 | Domain `BlankFinder` |
| I8 | Step A 우선 | 해 찾기 | n1 < n2 | D-SOL-01, I-INT-01 | Domain `StepABSolver` |
| I9 | Step B (reverse) on fail | 해 찾기 | n1 > n2 | D-SOL-02, I-INT-02 | Domain `StepABSolver` |
| I10 | 출력 = int[6], 1-index | 출력 계약 | length=6, r,c∈[1,4] | U-OUT-01, U-OUT-03, D-SOL-04~05 | Boundary + Domain |
| I11 | 둘 다 실패 → E005 | 도메인 실패 | E005 NO_VALID_MAGIC_SQUARE | D-SOL-03, U-OUT-02, I-INT-07 | Domain `StepABSolver` + Boundary |
| I12 | invalid 입력 시 Domain 호출 0회 | 가드 | mock spy `call_count == 0` | U-FLOW-02, I-INT-03~06 | Boundary `InputValidator` |

> **Traceability 무결성 규칙**: 위 표의 **모든 행에 최소 1개의 테스트 ID가 존재**해야 한다. 새 invariant 추가 시 행 추가 + 테스트 ID 채우기 = 동일 PR.

---

## 5. 컴포넌트 폴더 구조 (제안)

> 본 절은 워크북의 ECB(Entity·Control·Boundary) 명명 또는 일반적 Clean Architecture 명명 중 어느 쪽을 채택할지에 따라 조정. 두 옵션을 병기:

### 옵션 (i) — Clean Architecture 명명

```
src/
├── domain/         # Entity + Value Object + Domain Service
│   ├── constants.py        # GRID_SIZE, MAGIC_CONSTANT, etc.
│   ├── value_objects.py    # Coordinate, BlankCoordinates, MissingPair
│   ├── magic_board.py
│   ├── blank_finder.py
│   ├── missing_number_finder.py
│   ├── magic_square_validator.py
│   ├── solution_attempter.py
│   └── step_ab_solver.py
├── control/        # Use Case
│   └── solve_partial_magic_square.py
├── boundary/       # Adapter (입출력 경계)
│   ├── input_validator.py
│   ├── error_codes.py
│   └── solve_boundary.py
└── data/           # Repository 구현
    ├── matrix_repository.py    # Protocol/Interface
    ├── in_memory_repository.py
    └── file_repository.py      # Post-MVP
tests/
├── domain/         # D-*
├── boundary/       # U-*
├── data/           # DAT-*
└── integration/    # I-INT-*
```

### 옵션 (ii) — ECB (Entity / Control / Boundary) — 워크북 정렬

```
src/
├── entity/             # Domain (Entity·VO·Service 모두 여기)
│   └── ... (위와 동일 파일들)
├── control/            # Use Case
│   └── solve_partial_magic_square.py
└── boundary/           # 입출력 경계 + Data Adapter (워크북 ECB는 Data를 Boundary에 흡수)
    ├── input_validator.py
    ├── solve_boundary.py
    └── repository/
        ├── matrix_repository.py
        └── in_memory_repository.py
```

> **추천**: 워크북이 후속 단계에서 ECB 명명을 사용하므로 **(ii) ECB**를 채택. Data는 별도 폴더 대신 `boundary/repository/`로 흡수.

---

## 6. 다음 단계 진입 조건 (Definition of Ready for P-02)

본 보고서가 다음 단계(PRD 작성 §P-02)로 넘어가려면 다음을 만족해야 한다:

- [ ] 모든 invariant(I1~I12)가 §4.5 Traceability Matrix에 존재 + 최소 1 테스트 ID 매핑
- [ ] 모든 에러 코드(E001~E005)가 §2.2에 정의 + invariant와 매핑
- [ ] 모든 Domain Service의 시그니처가 §1.4에 명시
- [ ] §3.3에서 Data Layer 구현 옵션 선택 완료 (현재: A → B 순차)
- [ ] §5에서 폴더 구조 채택 완료 (현재: ECB 권장)
- [ ] 본 보고서 어디에도 구현 코드 0줄 (검증: grep `def ` 또는 `function` 0건 — 단, 시그니처 표기는 표 안에만)

---

## 7. 본 보고서가 의도적으로 미루는 결정

- **정확한 에러 메시지 문구** (예: `"Grid must be 4x4."` vs `"4×4 격자가 아닙니다."`) → P-02 PRD에서 확정
- **CLI/Web/Library 중 외부 노출 형태** → P-02 PRD에서 확정
- **Repository 구현체 선택 시점** → MVP는 InMemory, Golden Master 단계에서 File 추가
- **회전·반사 동치 처리** → Post-MVP (NG로 유지)
- **로깅·관측성** → 학습 프로젝트 범위 외

---

## 8. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — 워크북 §과제 1 프롬프트(L612~691) 실행 결과 |

# 4x4 Magic Square — TDD 학습 프로젝트

> 1부터 16까지의 숫자를 4×4 격자에 배치할 때 성립해야 하는 10개의 합 제약(가로 4 + 세로 4 + 대각선 2)을, **invariant 단위로 RGR(🔴RED → 🟢GREEN → 🔵REFACTOR) 사이클을 돌려가며** 형식 언어로 옮기는 학습용 프로젝트.

본 프로젝트의 본질은 "마방진을 푸는 코드"가 아니라, **"마방진의 판정 규칙을 검증 가능한 절차로 옮기는 경험"** 이다. 자세한 동기·전개는 아래 문서를 참조.

- [`Report/01_problem_definition.md`](./Report/01_problem_definition.md) — 5 Whys 기반 문제 정의 및 메타 invariant
- [`Report/02_branching_strategy.md`](./Report/02_branching_strategy.md) — RGR 정합 브랜치·커밋 전략
- [`Report/03_prd.md`](./Report/03_prd.md) — Product Requirements Document (persona·모드·CLI·MVP 경계)
- [`Prompt/01_problem_definition_transcript.md`](./Prompt/01_problem_definition_transcript.md) — 문제 정의 과정의 원본 대화 기록

---

## 핵심 Invariant

| #  | Invariant                                                                  |
| -- | -------------------------------------------------------------------------- |
| I1 | 격자의 값 집합 = {1, …, 16} (중복 없음, 누락 없음)                            |
| I2 | 각 가로행 4개의 합 = 34                                                     |
| I3 | 각 세로열 4개의 합 = 34                                                     |
| I4 | 두 대각선의 합 = 34                                                         |
| I5 | 34는 I1로부터 강제되는 파생값 (사용자가 정할 수 있는 자유도 아님)            |
| I6 | 마방진 성립 ⇔ I1~I4를 **동시에** 만족 (부분 성립 없음)                       |

> **메타 invariant**: 모드 A(퍼즐) ↔ 모드 B(데모)는 위 6개를 **동일한 정의로** 공유한다.

---

## 디렉터리 구조

```
.
├── Prompt/         # 문제 정의 과정의 원본 대화 기록
├── Report/         # 정제된 보고서 (문제 정의·브랜치 전략)
├── src/            # 도메인 코드 (작업 브랜치에서 추가, develop을 거쳐 main으로 머지)
├── tests/          # 테스트 — TDD 진입점
└── pyproject.toml
```

`main`은 **머지 시점의 통합 상태만** 담는다. 작업 중 코드는 `feature/<invariant-id>-*` 브랜치에 있다.

---

## 브랜치·커밋 규약 (요약)

> 자세한 정당화와 안티패턴은 [`Report/02_branching_strategy.md`](./Report/02_branching_strategy.md) 참조.

핵심 원칙: **브랜치 = invariant 단위 / 커밋 = RGR 단계 단위**

### 3-Layer 브랜치 구조

| 계층 | 이름 예시                              | 직접 커밋          | main으로의 머지 |
| ---- | -------------------------------------- | ------------------ | --------------- |
| 통합 | `main`                                 | ❌                 | —               |
| 개발 | `develop`                              | ⚠️ 문서 작업만 예외 | **코드 release 시에만** (문서 단독 머지 금지) |
| 작업 | `feature/<invariant-id>-<짧은-이름>`   | ✅                 | (develop으로 PR) |

> `main`은 **코드 변경이 포함된 release 머지만** 받는다. 문서(`Report/`, `Prompt/`, `README.md`)만 변경된 `develop`은 `main`으로 PR하지 않는다. 자세한 정책은 [`Report/02_branching_strategy.md` §2.1](./Report/02_branching_strategy.md) 참조.

작업 브랜치 예: `feature/I1-set-equality`, `feature/I2-row-sum`, `feature/I6-composite-judgment`, `feature/mode-A-puzzle`, `feature/M4-judgment-parity`

### 커밋 메시지 prefix

```
🔴 RED:      <테스트 이름>    — 실패하는 테스트 추가
🟢 GREEN:    <테스트 이름>    — 최소 구현으로 통과
🔵 REFACTOR: <범위>          — 동작 변경 없이 구조 개선
```

머지 전략: **rebase merge** — RGR 사이클을 `develop` 히스토리에 보존하여 **학습 일지** 로 삼는다.

---

## 실행

```bash
# 1) 가상환경
python -m venv .venv
source .venv/bin/activate

# 2) 테스트 (코드가 있는 작업 브랜치에서)
pytest
```

> Python ≥ 3.10 (pyproject.toml 참조)

---

## 진행 순서 (권장)

`feature/I1` → `feature/I2`·`I3`·`I4` (병렬 가능) → `feature/I6` → `feature/mode-A`·`mode-B` → `feature/M4-judgment-parity`

| 단계 | 브랜치                              | 사전 조건                |
| ---- | ----------------------------------- | ------------------------ |
| 1    | `feature/I1-set-equality`           | —                        |
| 2~4  | `feature/I2-row-sum` 외 2건          | I1 머지                  |
| 5    | `feature/I6-composite-judgment`     | I1~I4 머지               |
| 6~7  | `feature/mode-A-puzzle`, `mode-B-demo` | I6 머지              |
| 8    | `feature/M4-judgment-parity`        | 모드 A·B 머지            |

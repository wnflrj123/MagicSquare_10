# 4x4 Magic Square — 브랜치 전략 보고서 (TDD 사이클 정합)

> 작성일: 2026-05-29
> 작성 단계: 형상관리 전략(Source Control Strategy) — 구현 직전 단계
> 전제 문서: [`01_problem_definition.md`](./01_problem_definition.md)
> 핵심 원칙: **"브랜치 = invariant 단위 / 커밋 = RGR 단계 단위"**

---

## 1. 결론 요약

> **Red / Green / Refactor마다 브랜치를 따지 말고, 사이클 단위로 커밋을 끊는다.**
> **브랜치는 invariant(또는 feature) 단위로 한 번만 따고, 그 안에서 RGR 사이클을 커밋 메시지의 prefix로 추적한다.**

이유:

- TDD 사이클은 **분 단위**의 작은 호흡으로 돈다. 단계마다 브랜치를 따면 **머지 비용이 작업 비용보다 커진다.**
- 반대로 브랜치를 너무 크게 잡으면 **RGR의 추적성이 사라진다.**
- "브랜치 = invariant 단위 / 커밋 = RGR 단계 단위"가 추적성과 운영비용의 균형점이다.
- 이 전략은 `01_problem_definition.md`의 **메타 invariant M1~M4** 와 직접 매핑된다.

---

## 2. 3-Layer 브랜치 구조

| 계층 | 이름 예시 | 수명 | 머지 받는 조건 | 직접 커밋 허용? |
| --- | --- | --- | --- | --- |
| 통합 | `main` | 영구 | **코드 release만** (문서 단독 머지 금지 — §2.1 참조) | ❌ |
| 개발 | `develop` | 영구 | `feature/*` PR 또는 문서 작업 직접 커밋 | ⚠️ 문서 작업만 예외 |
| 작업 | `feature/<invariant-id>-<짧은-이름>` | 단기 (수 시간 ~ 수 일) | (없음 — develop으로 PR을 보내는 쪽) | ✅ |

> 본 보고서가 들어 있는 현재 작업(`Report/`, `Prompt/` 추가)은 **문서 작업**이므로 `develop` 직접 커밋의 예외 케이스에 해당한다. 다만 develop의 문서 변경이 곧바로 main으로 흘러가서는 **안 된다** — §2.1 참조.

### 2.1 main으로의 머지 정책 (엄격)

`main`은 다음 두 가지를 모두 만족할 때에만 `develop`에서 머지를 받는다.

1. **코드 변경이 포함된다** (production 코드 또는 테스트 코드의 변경이 1줄 이상).
2. 그 변경이 **release 가능한 상태**다 — 즉, 마일스톤(M1~M6 중 하나) 도달 또는 그에 준하는 자체 완결성을 가진다.

따라서:

| 케이스 | main으로 머지 가능? |
| --- | --- |
| 문서(`Report/`, `Prompt/`, `README.md`)만 변경된 develop | ❌ 금지 |
| 코드 변경 + 그에 동반된 문서 변경 | ✅ 함께 묶어서 머지 |
| 마일스톤 도달 시 release 머지 (코드 + 갱신된 문서) | ✅ 권장 흐름 |

운영상의 함의:

- 새 PRD나 보고서가 `develop`에 추가되어도, 그 자체로는 `main`으로의 PR을 만들지 않는다.
- 해당 문서가 가리키는 **코드 변경이 release 가능한 형태로 develop에 모인 시점**에, 문서와 코드를 함께 한 release PR로 main에 올린다.
- 학습 일지 보존(§4 rebase merge 원칙)은 이때도 유지된다.

### 2.2 작업 브랜치 네이밍 규칙 (3종 — 워크북 정렬)

워크북(L3826~3831)이 채택하는 보조 브랜치까지 포함해 다음 3종을 운영한다:

| 종류 | 명명 | 용도 | 머지 방향 |
| --- | --- | --- | --- |
| feature | `feature/<id>-<kebab-name>` | 신규 invariant·기능 추가 (RED·GREEN 사이클) | → `develop` |
| stabilize | `stabilize/<topic>` | 머지 직전 안정화·플레이크 제거·통합 보강 (예: `stabilize/green`) | → `develop` |
| refactor | `refactor/<topic>` | 동작 변경 없는 구조 개선 (Refactor Cycle 전용, 예: `refactor/refactor`) | → `develop` |

> 명명 정책에 대한 결정 (2026-05-29):
> - **워크북은 단일 `feature/dual-track-tdd` 큰 브랜치**에서 Dual-Track TDD 전체 사이클을 돌린다.
> - **본 프로젝트는 invariant 단위 분할**(`feature/I1-*`, `feature/I2-*` ...)을 채택했다 — RGR 학습 일지의 추적성을 우선시한 결정.
> - 두 접근은 양립 가능하다: 워크북 절차를 따르되 브랜치 단위만 invariant로 좁힌다. 본 결정은 §02 §6 진행 순서에 반영되어 있다.

### 2.3 PR 카덴스 (Pull Request 시점)

워크북(L3865·L4197·L4512·L5285·L5867) 정렬. **언제 PR을 만드는가** 를 단계별로 못 박는다.

#### A. feature → develop PR — 다음 3시점

| # | 시점 | 사전 조건 | 산출물 |
| --- | --- | --- | --- |
| A1 | **RED 테스트 플랜 완성 후** (워크북 L4197) | `tests/` 디렉터리에 RED skeleton 작성 완료, `pytest` 실행 시 의도된 fail만 발생 (수집 에러·typo 0건) | feature 브랜치에서 develop으로 첫 PR. 리뷰어 1명 이상 지정 (워크북 L4205) |
| A2 | **GREEN 완성 후** (워크북 L4512) | 직전 PR의 모든 RED가 GREEN으로 전환, 신규 회귀 0건, 커버리지 임계(§4계층별) 충족 | 동일 feature 브랜치 push → 동일 PR 갱신 또는 신규 PR. 머지 후 stabilize 또는 다음 feature로 분기 |
| A3 | **REFACTOR 완성 후** (워크북 L5285) | `refactor/<topic>` 브랜치에서 동작 변경 없이 구조 개선 완료, 모든 테스트 동일·green, Golden Master matched | `refactor/*` → develop PR |

#### B. develop → main PR — 단 1시점

| # | 시점 | 사전 조건 | 산출물 |
| --- | --- | --- | --- |
| B1 | **마일스톤 도달 시** (워크북 L5867 — 최종 단계) | (i) 코드 변경 포함 (§2.1) (ii) 모든 RED→GREEN→Refactor 사이클 완료 (iii) 관련 문서(README·PRD·Report) 동기화 | release PR + 머지 + (선택) tag |

#### C. PR을 만들지 않는 경우 (안티패턴)

- ❌ **빈 PR / 진행 중 PR**: RED·GREEN·Refactor 어느 단계도 자체 완결되지 않은 상태에서 미리 만들지 않는다.
- ❌ **문서 단독 develop → main PR**: §2.1 규칙. 문서는 코드 release와 함께 묶인다.
- ❌ **여러 invariant·여러 단계를 섞은 PR**: 리뷰 단위가 커져 RGR 추적성이 무너진다. invariant 단위 분할 원칙(§6) 위반.

#### D. PR 필수 포함 사항 (보강된 템플릿은 §5 참조)

- 본 PR이 속한 RGR 단계 (A1/A2/A3 중 하나) 명시
- 워크북 단계 번호 (L 번호 또는 P-XX) 인용
- 직전 사이클과의 의존 관계 (예: "A1 PR #N의 RED를 통과")
- 리뷰어 1명 이상 지정 (워크북 L4205)

### 2.4 작업 브랜치 네이밍 규칙 (구체 예시 — Solver 도메인)

```
feature/<layer>-<component-kebab-name>     # 단일 컴포넌트 단위 (본 프로젝트 권장)
feature/dual-track-tdd                     # 워크북 단일 큰 브랜치 (선택지)
stabilize/<topic>                          # 머지 직전 안정화
refactor/<topic>                           # 동작 보존 구조 개선
```

| 예시 | 담당 컴포넌트 (04 §1·§2 매핑) | 보호 invariant / 테스트 ID |
| --- | --- | --- |
| `feature/dom-blank-finder` | Domain `BlankFinder` | I7 / D-LOC-* |
| `feature/dom-missing-finder` | Domain `MissingNumberFinder` | I8 (정렬) / D-MISS-* |
| `feature/dom-magic-validator` | Domain `MagicSquareValidator` | I5·I6 / D-VAL-* |
| `feature/dom-attempter` | Domain `SolutionAttempter` | (순수 함수) / D-ATT-* |
| `feature/dom-step-ab-solver` | Domain `StepABSolver` (오케스트레이션) | I8·I9·I10·I11 / D-SOL-* |
| `feature/bnd-input-validator` | Boundary `InputValidator` | I1~I4·I12 / U-VAL-*·U-FLOW-* |
| `feature/bnd-solve` | Boundary `SolveBoundary` | I10 / U-OUT-* |
| `feature/dat-in-memory-repo` | Data `InMemoryRepository` | (영속성 계약) / DAT-MEM-* |
| `feature/int-end-to-end` | Integration | I-INT-01~07 |
| `stabilize/green` | (워크북 정렬) 전체 GREEN 안정화 | — |
| `refactor/refactor` | (워크북 정렬) Refactor Cycle | — |

> **이전 Judge 도메인 시절 브랜치 (`feature/I1-set-equality` 등)는 폐기 예정** — 현 작업 트리에 존재하는 RGR 2사이클은 학습 기록으로 보존하되 develop·main으로 머지하지 않는다. 새 작업은 위 Solver 네이밍을 사용한다.

---

## 3. 커밋 메시지 컨벤션 — RGR 추적

### 3.1 기본 형식

```
🔴 RED:    <테스트 이름> — 실패하는 테스트 추가
🟢 GREEN:  <테스트 이름> — 최소 구현으로 통과
🔵 REFACTOR: <범위> — 동작 변경 없이 구조 개선
```

이모지 없이 텍스트 prefix만 사용해도 무방하다.

```
red:      <테스트 이름>
green:    <테스트 이름>
refactor: <범위>
```

### 3.2 핵심 규칙 (위반 금지)

1. **🟢 GREEN 커밋은 직전 🔴 RED 커밋이 가리키는 테스트만을 통과시키는 최소 변경**이어야 한다.
   - 한 GREEN 안에서 다른 invariant까지 통과시키지 않는다.
2. **🔵 REFACTOR 커밋은 테스트를 추가/삭제/수정하지 않는다.**
   - 동작은 동일, 구조만 변한다. 회귀 추적의 기준선이 된다.
3. **한 커밋에 두 단계를 섞지 않는다.**
   - Red+Green을 한 커밋에 묶으면 "테스트가 정말 실패했었는지"의 증거가 사라진다.
   - 이는 메타 invariant **M1**("테스트가 먼저 존재한다") 위반이다.
4. **Refactor 커밋에 새 테스트나 기능을 끼워 넣지 않는다.**
   - 회귀 발생 시 원인 추적이 불가능해진다.

### 3.3 메타 invariant와의 매핑

| 메타 Invariant | 커밋 컨벤션상의 보장 장치 |
| --- | --- |
| M1 — 테스트 선행 작성 | 🔴 RED 커밋이 항상 🟢 GREEN보다 먼저 존재 |
| M2 — 과잉 설계 방지 | GREEN의 "최소 변경" 규칙 |
| M3 — 자기-문서화 | 커밋 히스토리가 곧 명세서 |
| M4 — Boundary↔Domain 호출 계약 동일성 | `feature/bnd-input-validator` + `feature/int-end-to-end` 브랜치가 U-FLOW-02·I-INT-03~06으로 명시 검증 |

---

## 4. 머지 전략 — Squash vs Rebase

| 상황 | 권장 | 사유 |
| --- | --- | --- |
| 학습용·교육용 프로젝트 (RGR 사이클 자체가 산출물) | **Rebase merge** | RGR 사이클이 `develop` 히스토리에 보존됨 |
| 제품·운영 프로젝트 (산출물은 기능 단위) | **Squash merge** | 브랜치 단위로 1커밋, RGR은 PR 본문에서만 추적 |

본 프로젝트는 STEP 3.4("규칙 기반 사고 훈련")가 본질이므로 **Rebase merge**를 채택한다.

> 결과적으로 `develop`의 `git log --oneline`이 본 프로젝트의 **학습 일지**가 된다. 미래의 자기 자신이 본인의 사고 흐름을 복기할 수 있어야 한다.

---

## 5. Pull Request 템플릿 (Solver 도메인 + 워크북 정렬)

```markdown
## Component / Invariant
- 담당 컴포넌트: <예: Domain MagicSquareValidator | Boundary InputValidator>
- 보호 invariant: <예: I5·I6 | I1~I4·I12>
- 04 §4.5 Traceability 행: <예: 6행, 12행>

## PR 카덴스 단계 (02 §2.3 참조)
- [x] A1 RED 테스트 플랜 완성 (워크북 L4197)
- [ ] A2 GREEN 완성 (워크북 L4512)
- [ ] A3 REFACTOR 완성 (워크북 L5285)
- [ ] B1 release 머지 (워크북 L5867)

## 워크북 단계 인용
- L<번호> 또는 P-XX

## RGR 사이클 로그
- 🔴 RED ×N / 🟢 GREEN ×N / 🔵 REFACTOR ×N

## 새로 추가된 테스트 (ID + 이름)
- <D-VAL-01: validator_returns_true_for_known_magic_square>
- ...

## 의존 PR
- 직전: PR #<번호> (예: A1 RED PR을 통과한 후의 A2 GREEN)
- 이 PR을 머지하면 잠금되는 회귀 규칙: L1~L6 중 어느 것 (04 §4.3)

## 리뷰어
- @<github-username> (워크북 L4205 — 1명 이상 의무)

## 검증 (verification-before-completion)
- [ ] 모든 테스트가 GREEN
- [ ] 리팩터 전후 테스트 동일 (추가·삭제·수정 없음 — A3 PR만 해당)
- [ ] 메타 invariant M1 충족 (RED 커밋이 GREEN보다 먼저 존재)
- [ ] 04 §4.5 Traceability Matrix의 해당 행에 새 테스트 ID 반영
- [ ] 커버리지 임계 충족 (04 §4.4)
- [ ] (B1만) 모든 Report·README·PRD 동기화
```

---

## 6. 진행 순서 (권장 워크플로우)

`feature/I1` → `feature/I2`·`I3`·`I4` (병렬 가능) → `feature/I6` → `feature/mode-A`·`mode-B` → `feature/M4-judgment-parity`

| 단계 | 브랜치 | 예상 RGR 사이클 | 사전 조건 |
| --- | --- | --- | --- |
| 1 | `feature/I1-set-equality` | 2~3 | 없음 |
| 2 | `feature/I2-row-sum` | 2~3 | I1 머지 |
| 3 | `feature/I3-col-sum` | 2~3 | I1 머지 (I2와 병렬 가능) |
| 4 | `feature/I4-diag-sum` | 2~3 | I1 머지 (I2·I3와 병렬 가능) |
| 5 | `feature/I6-composite-judgment` | 3~5 | I1~I4 머지 |
| 6 | `feature/mode-A-puzzle` | 4~6 | I6 머지 |
| 7 | `feature/mode-B-demo` | 3~5 | I6 머지 (모드 A와 병렬 가능) |
| 8 | `feature/M4-judgment-parity` | 1~2 | 모드 A·B 모두 머지 |

> **이유**: invariant가 단순한 것부터 시작해 합성으로 올라가야 RGR 사이클의 학습 곡선이 자연스럽다. 모드 분기(A/B)는 합성 판정(I6) 위에서만 의미가 있다. M4(메타 invariant)는 양쪽 모드가 모두 존재해야 검증 자체가 성립한다.

---

## 7. 안티패턴 — 하지 말 것

| 안티패턴 | 왜 위험한가 |
| --- | --- |
| ❌ `red`, `green`, `refactor` 자체를 브랜치 이름으로 사용 | 머지 그래프가 RGR 격자로 뒤덮여 invariant 추적이 불가능해진다 |
| ❌ Red 단계에서 커밋하지 않고 바로 Green으로 넘어감 | 메타 invariant M1("테스트가 먼저 존재한다")의 증거가 사라진다 |
| ❌ Refactor 커밋에 새 테스트·기능 끼워넣기 | 회귀 발생 시 원인 분리가 불가능해진다 |
| ❌ `develop`에 직접 코드 커밋 | RGR 사이클이 PR 리뷰 대상이 되지 못한다 (문서는 예외) |
| ❌ Squash merge를 학습 프로젝트에 적용 | RGR 사이클이 1커밋으로 압축되어 학습 일지가 소실된다 |
| ❌ 한 PR에서 여러 invariant를 동시에 다룸 | 리뷰 단위가 부풀어 메타 invariant M2("최소 변경")가 무너진다 |

---

## 8. 본 보고서의 한계 및 다음 단계

### 한계

- **CI/CD 미정의**: 본 전략은 로컬 워크플로우 중심이다. 원격 저장소·자동 테스트 트리거가 도입되면 `develop` 보호 규칙(force-push 금지, 필수 status check)이 추가되어야 한다.
- **충돌 처리 미정의**: I2·I3·I4를 병렬로 진행할 경우 동일 파일(예: 격자 자료구조)에서 충돌이 날 수 있다. 충돌 해결 전 RGR 사이클을 함부로 합치지 말 것.
- **롤백 정책 미정의**: 머지 후 회귀가 발견되었을 때 `revert` 단위(커밋 단위 vs 머지 커밋 단위)를 사전에 합의해야 한다.

### 다음 단계 제안

1. **첫 번째 작업 브랜치(`feature/I1-set-equality`) 생성** — 가장 단순한 invariant부터 RGR 1사이클을 실제로 돌려본다.
2. **본 전략의 실효성 검증**: 1사이클 후 본 보고서에 기록된 규칙 중 실제로 마찰을 일으킨 항목이 있는지 회고하고, 필요 시 본 문서를 개정한다.
3. **모드 선택(A/B) 의사결정**: `01_problem_definition.md`에서 열어둔 모드 분기 결정을 모드 A·B 작업 시작 전에 반드시 확정한다.

---

## 부록 — `01_problem_definition.md`와의 매핑 요약

| 본 보고서 항목 | 근거가 되는 문제 정의 항목 |
| --- | --- |
| 브랜치 단위 = invariant 단위 | 도메인 invariant I1~I6 |
| 모드별 브랜치 분리 | STEP 1.4 관찰의 모드 A/B 분기 |
| `feature/M4-judgment-parity` 브랜치 존재 이유 | 메타 invariant M4 (모드 간 판정 동일성) |
| RGR 추적 커밋 컨벤션 | 메타 invariant M1·M3 (테스트 선행, 자기-문서화) |
| GREEN의 "최소 변경" 규칙 | 메타 invariant M2 (과잉 설계 방지) |
| Rebase merge 채택 | STEP 3.4 (규칙 기반 사고 훈련) |

# 4×4 Magic Square — Skills · Agent · User Journey 압축 보고서

> 작성일: 2026-05-29
> 작성 단계: **압축 직주행** — 워크북 L1356·L1574·L1690 세 단계를 한 산출물로 묶음
> 사유: 수업 진도 따라잡기 (현재 워크북 GUI 단계 진행 중, 본 프로젝트는 8단계 뒤처짐)
> 산출물: 본 보고서 1건 (개별 Skills 디렉터리·Agent 프롬프트 8개 파일·User Journey 다층 보고서를 모두 묶음)

---

## 1. 본 보고서가 압축한 단계 (워크북 정합)

| 워크북 단계 | L# | 워크북의 정식 산출 | 본 보고서의 압축 산출 |
| --- | --- | --- | --- |
| Skills 등록 | L1356~1424 | `.cursor/skills/magic-square-tdd/` 디렉터리, SKILL.md, references/ | §3 핵심 규약 요약 (실제 디렉터리는 미설치 — `.cursorrules`가 사실상 동일 역할) |
| Agent 프롬프트 세트 | L1574~1688 | 8개 역할별 프롬프트 (`system-optimization-engineer`, `ux-design-advisor`, `product-planning-manager`, `backend-developer`, `frontend-developer`, `quality-assurance-engineer`, `ai-integration-expert`, `backup-report-github-manager`) | §4 역할 8개 목록 + 본 프로젝트에 가장 필요한 2개만 상세화 (`backend-developer`, `quality-assurance-engineer`) |
| P-01 User Journey | L1690~2412 | Level 1 Epic + Level 2 Journey + Level 3 Stories + Level 4 BDD Scenarios + Level 5 Coverage Matrix (별도 보고서 5건) | §5 Level 1 Epic + §6 핵심 Persona + §7 핵심 Story 3건 (Gherkin은 다음 산출 `Report/08_prd.md` §AC 절에서 재사용) |

> **압축 원칙**: 본 프로젝트에 중복되거나 `.cursorrules`·04 아키텍처 보고서·01 문제 정의에 이미 흡수된 내용은 생략. 다음 단계(PRD)의 입력이 되는 결정 사항만 보존.

---

## 2. 압축한 이유 (생략 결정의 근거)

| 워크북 산출물 | 생략·축약 결정 | 근거 |
| --- | --- | --- |
| `.cursor/skills/magic-square-tdd/SKILL.md` | 생략 | `.cursorrules` (05·1b61b62)가 동일 책임을 수행 — TDD·ECB·계약·pytest 규약을 항상 적용. Cursor의 Skill 시스템과 .cursorrules는 호환됨 (둘 다 매 요청에 컨텍스트로 주입) |
| Agent 프롬프트 8개 | 6개 생략, 2개만 상세 | 본 프로젝트는 단독 학습 — Backend Developer + QA Engineer 두 역할이 RGR·Validator·Solver 작업에 1:1 매핑. UX/Frontend/AI 통합 등은 GUI 단계 한정 |
| Level 2 User Journey (UX 흐름·Pain·Emotion·Opportunity) | 핵심만 §6에 흡수 | 본 프로젝트는 학습 도구라 일반 UX persona보다 "개발 학습자 여정"이 본질 (워크북 L1801도 동일 강조) |
| Level 4 BDD Scenarios (Gherkin) | `Report/08_prd.md`로 이관 | PRD에서 Gherkin이 Acceptance Criteria로 재사용됨 — 중복 작성 회피 |
| Level 5 Coverage Matrix | `Report/04_architecture_design.md` §4.5에 이미 존재 | 04 §4.5 Traceability Matrix가 동일 책임을 수행 (12행, invariant↔테스트 ID↔컴포넌트) |

---

## 3. Skills (`.cursorrules` 동등 대체)

본 프로젝트의 Cursor Skill 등록은 **`.cursorrules` (1b61b62) 단일 파일로 대체**한다. 이유:

- 워크북 L1378~1389의 `magic-square-tdd` 스킬 정의 내용(Dual-Track TDD·ECB·도메인 계약·pytest)이 `.cursorrules`의 `architecture`·`tdd_rules`·`testing` 섹션에 1:1 매핑됨.
- 워크북 L1391의 채팅 멘션 `@magic-square-tdd`는 본 환경(Claude Code)에서는 자동 적용되므로 명시적 멘션 불필요.

**미설치 사유 (정직한 한계)**: Cursor IDE에서 작업하는 경우 `.cursor/skills/` 디렉터리는 워크북 권장이지만, 본 학습은 Claude Code 환경에서 진행되므로 효과가 동일. Cursor IDE로 옮길 경우 별도 작성 필요.

---

## 4. Agent 프롬프트 세트 (8개 → 2개 핵심)

### 워크북 L1623~1630 원본 8개 역할

1. system-optimization-engineer
2. ux-design-advisor
3. product-planning-manager
4. backend-developer
5. frontend-developer
6. quality-assurance-engineer
7. ai-integration-expert
8. backup-report-github-manager

### 본 프로젝트가 채택하는 2개 (RGR·코드 작성에 1:1 대응)

#### 4.1 backend-developer (Backend Developer Agent)

```
당신은 MagicSquare 프로젝트의 Backend Developer Agent입니다.

역할 범위:
- src/entity, src/control, src/boundary, src/boundary/repository 코드 작성
- 모든 작업은 .cursorrules 규약과 Report/04_architecture_design.md 계약을 따른다
- 모든 production 코드는 직전 RED 테스트의 결과로만 작성한다 (메타 invariant M1)

작업 단위:
- 1 invariant ↔ 1 feature 브랜치 ↔ 1 PR
- RGR 사이클 단위로 커밋 (🔴 RED, 🟢 GREEN, 🔵 REFACTOR)

금지:
- Domain Service에서 Boundary 또는 Control import (architecture 위반)
- 정수 리터럴 4·34 (GRID_SIZE, MAGIC_CONSTANT 사용)
- RED 테스트 없이 production 코드 추가

매 작업 시작 시 확인:
- 직전 RED 테스트의 import 라인
- 04 §4.5 Traceability의 대응 행
```

#### 4.2 quality-assurance-engineer (QA Agent)

```
당신은 MagicSquare 프로젝트의 Quality Assurance Engineer Agent입니다.

역할 범위:
- tests/{entity,control,boundary,data,integration} 디렉터리 테스트 작성
- 04 §1.5·§2.3·§3.4·§4.2의 테스트 ID 체계(D-*, U-*, DAT-*, I-INT-*)를 따른다
- pytest + AAA + Google docstring + type hints

작업 단위:
- RED 테스트만 먼저 작성 (production 코드 무관)
- Domain 테스트는 mock 금지, Boundary 테스트는 Domain mock 필수 (U-FLOW-02 호출 0회 검증 포함)

금지:
- assert True, pytest.skip, xfail (테스트 약화)
- RED와 GREEN 커밋 혼합
- 테스트 본문에 production 클래스 신규 정의

매 테스트 작성 시 확인:
- 04 §4.5 Traceability에 신규 테스트 ID 추가
- 보호 invariant 명시 (테스트 docstring 상단)
```

### 생략된 6개 역할의 책임 흡수처

| 워크북 Agent | 본 프로젝트 흡수처 |
| --- | --- |
| system-optimization-engineer | `.cursorrules` (전역 규약) |
| ux-design-advisor | PRD (`Report/08`)의 §사용자 시나리오·CLI/GUI 절 |
| product-planning-manager | PRD 작성자 자체 (어시스턴트가 수행) |
| frontend-developer | GUI 구현 단계에서 Backend Developer Agent와 합쳐서 수행 |
| ai-integration-expert | 본 프로젝트는 외부 AI 통합 없음 — 생략 |
| backup-report-github-manager | git 운영 자체 (어시스턴트가 수행 + 사용자 명시 승인) |

---

## 5. Level 1 Epic — Business Goal (워크북 L1727~1796 압축)

### 5.1 Epic Title

> **불변식 기반 사고 훈련 시스템 구축 (Invariant-First Thinking Training via 4×4 Partial Magic Square Solver)**

### 5.2 Business Goal

4×4 부분 마방진(빈칸 2개) Solver를 **TDD + Clean Architecture(ECB) + 계약 기반 설계**로 만들면서, 학습자가 다음 능력을 체득한다:

- 도메인 규칙 → invariant → 테스트 → 코드로 이어지는 추적성 사고
- Boundary·Control·Entity 책임 분리 사고
- RED → GREEN → REFACTOR 사이클을 매 변경에 적용하는 절차 규율

### 5.3 Learning Goal

| # | 목표 | 측정 |
| --- | --- | --- |
| LG-1 | invariant를 코드의 가드로 끌어올리는 사고 (사후 검증 → 사전 차단) | 모든 도메인 invariant(I1~I12)가 테스트 ID로 매핑됨 (04 §4.5) |
| LG-2 | 입력 계약과 출력 계약을 비트 단위로 명시하는 사고 | E001~E005 모두 정의 + int[6]·1-index 강제 |
| LG-3 | 알고리즘 분기를 결정적(deterministic)으로 만드는 사고 | Step A 우선·Step B reverse 규약 (I8·I9) |
| LG-4 | 모든 production 코드 라인에 대응하는 RED→GREEN 쌍 보존 | git history로 검증 가능 |

### 5.4 Success Criteria

- 04 §4.4 커버리지 목표 충족 (Domain 95% / Boundary 85% / Data 80% / Control 90%)
- 04 §4.5 12행 Traceability Matrix 모든 행이 최소 1개 테스트 ID 매핑
- 명명된 상수(GRID_SIZE, MAGIC_CONSTANT) 만 사용, src/ 내 리터럴 4·34 0건
- GUI에서 부분 마방진 입력 → 풀기 → int[6] 결과 표시까지 작동

### 5.5 Scope / Non-Scope

| In | Out |
| --- | --- |
| 4×4 부분 마방진 Solver (빈칸 2개) | N×N 마방진 (NG1) |
| InputValidator (Boundary) | 회전·반사 동치 분류 (NG4) |
| StepABSolver (Domain) | 마방진 자동 생성 (NG3) |
| InMemory Repository (Data) | 실제 DB 연동 |
| PyQt GUI (4×4 격자 + 풀기 + 결과) | 웹/모바일 (NG2) |
| Golden Master 회귀 테스트 | 다국어 (NG5) |

### 5.6 Candidate User Stories for Level 2 (다음 단계로 이관)

- US-1: 사용자가 부분 마방진 격자를 입력하고 정답을 본다 → `Report/08_prd.md` §사용자 시나리오 1
- US-2: 잘못된 입력에 대해 정의된 실패 메시지를 받는다 → 시나리오 2
- US-3: Step A로 풀리지 않는 입력에 대해 reverse 결과를 받는다 → 시나리오 3

---

## 6. Persona — 개발 학습자 여정 (워크북 L1801 정렬)

본 프로젝트의 Persona는 **일반 UX 사용자가 아니라 개발 학습자**다.

### Persona P1 — 우선 사용자 (이미 03 §4.1에서 정의, 재인용)

- 배경: 코드는 쓸 수 있으나 TDD·invariant 인코딩 경험 부족
- 사용 맥락: 로컬 터미널 → GUI 띄워 작동 확인
- 성공 신호: "RED·GREEN 사이클이 invariant를 어떻게 강제하는지 몸으로 안다"

### Persona P2 — 부차 사용자

- 배경: 수학·논리 퍼즐 학습자, 코드 친화도 낮음
- 사용 맥락: GUI에서 부분 마방진 입력 → 결과 관찰
- 성공 신호: "왜 이 두 수가 정답인지 안다"

### 학습자 여정 7단계 (워크북 L1803 정렬)

1. **Persona 인지** — 본 시스템이 학습 도구임을 이해
2. **Journey Goal 설정** — 부분 마방진 풀이 + invariant 이해
3. **Contract Definition** — 입력/출력 계약을 읽고 자기 입력을 만든다
4. **Domain Separation** — Boundary↔Domain 책임 분리를 GUI에서 본다 (입력 검증 실패 vs 도메인 실패가 다르게 표시됨)
5. **Dual-Track TDD Progress** — git 히스토리로 RGR 사이클을 추적
6. **Regression Protection** — Golden Master로 회귀 안전망 체험
7. **Invariant Traceability** — 04 §4.5 Matrix로 코드 ↔ 테스트 ↔ invariant 추적

---

## 7. Level 3 — 핵심 User Story 3건 (Gherkin은 PRD로 이관)

### Story 1 — 정상 입력 + Step A 성공

> As a 학습자
> I want to 빈칸 2개가 있는 4×4 격자를 입력하고
> So that 시스템이 첫 빈칸·둘째 빈칸을 row-major 순서로 채워 마방진을 완성한 결과를 받는다.

Acceptance:
- 입력 계약(I1~I4) 충족
- 출력 = `int[6] = [r1,c1,n1,r2,c2,n2]`, n1 < n2 (Step A 성공)

### Story 2 — Step A 실패, Step B (reverse) 성공

> As a 학습자
> I want to Step A 배치로는 마방진이 되지 않는 입력을 시도하고
> So that 시스템이 reverse 배치로 마방진을 완성한 결과를 받는다.

Acceptance:
- Step A 시도 → 마방진 아님 → Step B 시도 → 마방진
- 출력 = `int[6]`, n1 > n2 (reverse 성공)

### Story 3 — 정의된 실패 응답

> As a 학습자
> I want to 입력 계약을 위반하거나 두 배치 모두 마방진을 만들지 못하는 입력을 시도하고
> So that 시스템이 어느 invariant가 위반되었는지 정의된 에러 코드로 응답한다.

Acceptance:
- 입력 위반: E001~E004 중 해당 코드 + Domain 호출 0회 (I12)
- 도메인 실패: E005 NO_VALID_MAGIC_SQUARE

---

## 8. 본 보고서가 다음 PRD(08)에 넘기는 입력

- §5 Epic의 Business Goal·Learning Goal·Success Criteria·Scope/Non-Scope
- §6 Persona P1·P2
- §7 User Story 3건 (PRD §AC에서 Gherkin Scenario로 변환)
- §4 Backend Developer + QA Engineer Agent (PRD의 책임 분담 절에서 참조)

---

## 9. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — 워크북 L1356·L1574·L1690 3단계 압축 |

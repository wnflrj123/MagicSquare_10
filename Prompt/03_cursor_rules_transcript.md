# Prompt Transcript — Cursor Rules 설계 세션

> 내보낸 날짜: 2026-05-29
> 브랜치: develop
> 세션 주제: 워크북 §"MagicSquare Python 프로젝트용 Cursor Rule" (L702~917) 실행
> 산출물: [`.cursorrules`](../.cursorrules) (루트, YAML), [`Report/05_cursor_rules_design.md`](../Report/05_cursor_rules_design.md)

---

## 📌 세션 컨텍스트

- 작업 디렉토리: `/Users/juri/Projects/sec_cursor/MagicSquare_1130`
- 출처 문서: `../CursorAI/응용-...실습-워크 북.docx` (L702~917)
- 직전 산출물 (develop): 01·02(§2.3 카덴스 포함)·04, ~~03 (SUPERSEDED)~~
- 트리거: "다음. 그리고 PR올려야할때 올려줘"

---

## 1️⃣ 워크북 §"Cursor Rules" — 4단계 프롬프트 패턴

워크북은 Cursor Rules 작성을 **4단계 점진적 프롬프트**로 권장한다:

| 단계 | 워크북 위치 | 목적 |
| --- | --- | --- |
| 0 (설계 방향 요청) | L707~726 | 파일 구조·`.cursorrules` vs `.mdc` 선택 결정 |
| 1 (뼈대 생성) | L735~739 | 최상위 8개 키만, 값은 비워둠. 80자 구분선 주석 |
| 2 (섹션별 채우기) | L751~755 | tdd_rules부터 시작 |
| 3 (검토 요청) | L766~772 | 문법 오류·누락·충돌·실현 가능성 검증 |
| 4 (이어서 작성) | L785~828 | 8섹션을 한 번에 채우기 — 각 섹션별 상세 요구사항 |

본 세션은 **단계 0~4를 단일 호흡으로 통합 실행** (시간 효율화 + 산출물의 일관성 확보).

---

## 2️⃣ 워크북 프롬프트 (verbatim, L735~828의 통합 단계 4)

```
위에서 만든 .cursorrules 뼈대의 빈 섹션을 모두 채워줘.
MagicSquare 프로젝트 기준으로 작성해.

각 섹션 작성 규칙:

code_style:
- python_version: "3.10+"
- style_guide: PEP8 엄격 준수
- type_hints: 모든 함수 파라미터와 반환값에 필수
- docstring: Google 스타일, 모든 public 메서드에 필수
- max_line_length: 88 (Black 기준)

architecture:
ECB 패턴 3 레이어를 각각 정의해줘:
- boundary: 외부 입출력 담당 (UI, API, CLI)
- control: 비즈니스 로직 담당
- entity: 도메인 데이터 및 규칙 담당
레이어 간 의존성 방향도 명시해줘.

tdd_rules:
지금은 문자열 1줄인데, 하위 항목으로 세분화해줘.
각 phase마다:
- description: 단계 설명
- rules: 지켜야 할 규칙 목록
- must_not: 이 단계에서 하면 안 되는 것

testing:
- framework: pytest
- pattern: AAA (Arrange-Act-Assert)
- coverage_minimum: "80%"
- fixture_scope: 규칙 정의
- naming_convention: test_ 접두사 필수

forbidden:
항목마다 아래 구조로 작성:
pattern: 금지 패턴
reason: 금지 이유
alternative: 대신 써야 할 것
최소 포함 항목: print(), 하드코딩 상수, except 단독 사용

file_structure:
ECB 기준 폴더 구조를 트리 형태 주석으로 작성해줘.
boundary/, control/, entity/, tests/ 포함.

ai_behavior:
Cursor AI가 코드 생성 전·중·후에 반드시 따라야 할 규칙.
최소 포함:
- 코드 작성 전 관련 테스트 파일 확인
- ECB 레이어 경계 위반 금지
- 타입힌트 없는 함수 생성 금지
- tdd_rules 위반 시 경고 출력

완성된 .cursorrules 전체 파일을 출력해줘.
```

추가 사용자 지시 (워크북 L915~917):

> 다음의 순서로 실행해줘
> 1. Report 폴더에 보고서 생성해줘
> 2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘

---

## 3️⃣ 어시스턴트 응답 요약

### 입력 분석

- 워크북의 최소 요구를 충족하면서, 본 프로젝트가 이미 산출한 04 아키텍처 보고서·02 PR 카덴스의 결정을 `.cursorrules`에 정적 인코딩한다 — Cursor가 매 요청마다 04·02를 재해석하지 않게.
- `.cursorrules` vs `.cursor/rules/*.mdc`: 워크북 정렬 + 작은 규모 = `.cursorrules` YAML 단일 파일 채택.

### 산출 구조

- `.cursorrules` (루트, YAML, 8섹션 + 80자 구분선)
- `Report/05_cursor_rules_design.md` — 설계 의도·자기 검증·한계·진화 경로 7장
- 본 전사본

### 본 세션의 단독 결정 (워크북 외 추가)

| ID | 결정 | 사유 |
| --- | --- | --- |
| ADD-1 | `project.authoritative_docs` | 다중 보고서 환경에서 정본 명시 필요 |
| ADD-2 | `project.superseded_docs` | 03 PRD가 살아 있으나 참조 금지임을 인코딩 |
| ADD-3 | `code_style.literal_constants.forbidden_literals_in_src: [4, 34]` | 04 §1.2 I5 (Magic Constant SSOT) 정적 인코딩 |
| ADD-4 | `testing.test_id_namespaces` (D/U/DAT/I-INT) | 04와 동기화 |
| ADD-5 | `testing.mocking_policy` 세분화 | 04 §1.4·§2.3 Domain mock 금지 vs Boundary Domain mock 강제 |
| ADD-6 | `forbidden`에 6개 패턴 추가 (총 9개) | 04·02의 안티패턴을 forbidden에 끌어올림 |
| ADD-7 | `ai_behavior.on_workbook_step_completion` | 워크북 단계마다 Report+Prompt 페어 자동 산출 |
| ADD-8 | `ai_behavior.on_tdd_violation.detection_signals` | TDD 위반 신호 3종 명시 |

### 자기 검증 (워크북 L766~772 항목)

| 항목 | 결과 |
| --- | --- |
| YAML 문법 오류 | ✅ Pass |
| 누락 섹션 | ✅ Pass (8개 모두) |
| `tdd_rules` ↔ `forbidden` 충돌 | ✅ Pass (강조 중복은 충돌 아님) |
| AI가 따를 수 없는 규칙 | ⚠️ `ai_behavior.after_writing_code.pytest 자동 실행`은 환경 의존 — 보고서 §3에 명시 |

---

## 4️⃣ PR 결정

본 세션 산출물은 **문서 + 설정 파일(.cursorrules)** 만이다. 02 §2.1·§2.3 규칙 적용:

- ❌ main으로의 PR **만들지 않음** — 코드 변경 없음 (§2.1)
- ❌ feature → develop PR **만들지 않음** — 02 §2.1 예외로 develop 직접 커밋 허용 (문서 작업)
- develop으로 직접 커밋 + push만 수행

> `.cursorrules`는 production 코드가 아니라 AI 에이전트 설정이므로 02 §2.1의 "코드 release" 정의에서 제외된다고 해석.

---

## 5️⃣ 산출물 인덱스 (누적)

| # | 파일 | 역할 |
| --- | --- | --- |
| 1 | `.cursorrules` | **본 세션 산출** — Cursor AI 규약 (8섹션) |
| 2 | `Report/01_problem_definition.md` v2.0 | Solver 도메인 문제 정의 |
| 3 | `Report/02_branching_strategy.md` | 브랜치·PR 카덴스 (§2.3 신규) |
| 4 | `Report/03_prd.md` | ⚠️ SUPERSEDED |
| 5 | `Report/04_architecture_design.md` | ECB·테스트 ID·Traceability |
| 6 | `Report/05_cursor_rules_design.md` | **본 세션 산출** — Cursor Rules 설계 의도 |
| 7 | `Prompt/01_problem_definition_transcript.md` | 01 세션 |
| 8 | `Prompt/02_architecture_design_transcript.md` | 04 세션 |
| 9 | `Prompt/03_cursor_rules_transcript.md` | **본 세션 전사** |

---

## 6️⃣ 다음 단계 (워크북 기준)

워크북 §"ECB 폴더 스켈레톤 + User Entity 워밍업" (L856~917). 본격적으로 **production 코드 산출**이 시작되며:

- `src/entity/`·`src/control/`·`src/boundary/` 디렉터리 생성
- `src/entity/user.py` (워밍업 예제) 작성 — `.cursorrules`의 정상 동작 검증을 겸함
- 워밍업 단계의 RED 의무 여부 결정 필요 (`.cursorrules` ai_behavior와 충돌 가능성)

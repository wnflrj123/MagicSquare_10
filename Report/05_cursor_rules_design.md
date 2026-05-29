# 4×4 Magic Square — Cursor Rules 설계 보고서

> 작성일: 2026-05-29
> 작성 단계: AI 에이전트 규약 정의(Agent Rules) — 워크북 §"MagicSquare Python 프로젝트용 Cursor Rule" (L702~917)의 산출물
> 산출 파일: [`.cursorrules`](../.cursorrules) (프로젝트 루트, YAML)
> 전제 문서:
> - [`Report/01_problem_definition.md`](./01_problem_definition.md) v2.0
> - [`Report/02_branching_strategy.md`](./02_branching_strategy.md) §2.3 PR 카덴스 (방금 반영)
> - [`Report/04_architecture_design.md`](./04_architecture_design.md) — ECB·테스트 ID·Traceability

---

## 1. 설계 결정 (Architecture of the Rules File)

### 1.1 `.cursorrules` vs `.cursor/rules/*.mdc` 중 선택

| 항목 | `.cursorrules` (단일 YAML) | `.cursor/rules/*.mdc` (분할 MDC) |
| --- | --- | --- |
| 도입 시점 | Cursor 초기부터 지원 (legacy) | 최신 Cursor (2024+) |
| 형식 | YAML 단일 파일 | Markdown + frontmatter, 다중 파일 |
| 학습 곡선 | 낮음 (YAML 한 파일) | 중간 (frontmatter `globs`·`alwaysApply` 필요) |
| 적용 단위 | 전 프로젝트 일괄 | 파일/디렉터리별 선택 적용 가능 |
| 워크북 채택 | ✅ 워크북 L735는 `.cursorrules` YAML 사용 | ❌ |

> **결정**: `.cursorrules` (YAML) 채택. 워크북 절차와 1:1 정합되며, 본 프로젝트는 ECB 3계층 + 통합 5개 폴더라는 작은 규모라 단일 파일로 충분.
>
> **부수효과 고려**: 최신 Cursor가 `.cursor/rules/*.mdc`를 우선 처리하더라도 `.cursorrules`는 fallback으로 인식된다. 추후 규약이 비대해지면 분할 마이그레이션 가능 (본 보고서 §5 참조).

### 1.2 8개 최상위 섹션 — 워크북 정합

워크북 L737이 지정한 최상위 키 순서를 그대로 채택:

```
project, code_style, architecture, tdd_rules, testing, forbidden, file_structure, ai_behavior
```

각 섹션 사이에 `# ==...===` 80자 구분선 주석 (워크북 L738 요구사항).

### 1.3 본 보고서가 워크북 외에 추가한 결정

| # | 결정 | 사유 |
| --- | --- | --- |
| ADD-1 | `project.authoritative_docs` 필드 신설 | Cursor가 매 요청마다 어느 보고서를 정본으로 봐야 하는지 명시. 워크북에는 없으나 다중 보고서 환경에서 필수. |
| ADD-2 | `project.superseded_docs` 필드 신설 | `Report/03_prd.md`가 살아 있으나 참조 금지임을 AI에게 강제 알림 |
| ADD-3 | `code_style.literal_constants.forbidden_literals_in_src: [4, 34]` | 04 §1.2 I5 (Magic Constant SSOT)를 정적 규약으로 인코딩 |
| ADD-4 | `testing.test_id_namespaces` | D/U/DAT/I-INT 4종 네임스페이스를 04와 동기화 |
| ADD-5 | `testing.mocking_policy` | Domain 테스트의 mock 금지 + Boundary 테스트의 Domain mock 허용 — 04 §1.4·§2.3 정합 |
| ADD-6 | `forbidden`의 8번째·9번째 패턴 (RED 없이 코드·테스트 약화·PR 혼합) | 02 §2.3 안티패턴을 forbidden 섹션으로 끌어올림 |
| ADD-7 | `ai_behavior.on_workbook_step_completion` | 워크북 단계마다 Report+Prompt 페어 산출 + README 인덱스 갱신을 자동화 |
| ADD-8 | `ai_behavior.on_tdd_violation.detection_signals` | TDD 위반 신호 3종(RED 없는 코드·혼합 commit·refactor에 테스트 변경)을 명시 |

---

## 2. 섹션별 설계 의도

### 2.1 `project`

**의도**: 프로젝트 정체성과 도메인 핵심 사실을 한 곳에 못 박는다. Cursor가 매 요청마다 "이 프로젝트가 뭐 하는 곳인가"를 다시 추론하지 않게 한다.

핵심 필드:
- `name: MagicSquare` (워크북 L1601 정렬)
- `description`: Solver 도메인 1단락 요약 (01 §5.2의 결정 정의 요약)
- `authoritative_docs` / `superseded_docs`: 본 프로젝트 다중 보고서 환경 대응

### 2.2 `code_style`

**의도**: PEP8 위에 본 프로젝트 고유 강제 규약을 얹는다.

핵심 결정:
- `python_version: "3.10+"` (워크북 L711, pyproject.toml 정합)
- `type_hints.required_on`: 함수·메서드의 파라미터·반환 4곳 모두 (워크북 L791 정합)
- `docstring.style: Google` (워크북 L792)
- `max_line_length: 88` Black 기준 (워크북 L793)
- **`literal_constants.forbidden_literals_in_src: [4, 34]`** — 04 §1.2 I5 위반 정적 검출

### 2.3 `architecture`

**의도**: ECB 3계층의 책임·경로·의존 방향을 코드로 인코딩.

핵심 규약:
- `boundary` → `control` → `entity` (안쪽이 더 안정)
- `boundary.may_not_depend_on: [entity]` — Domain Service 직접 호출 금지 (반드시 Control 경유)
- `entity.may_depend_on: []` — Domain은 표준 라이브러리 외 의존 금지 (04 §4.1 규칙)

Cursor가 위 경계를 위반하는 import 추가 시 `ai_behavior.while_writing_code` 규약에 의해 즉시 중단되어야 한다.

### 2.4 `tdd_rules`

**의도**: 02 §3.2 핵심 규칙 4개를 AI 에이전트가 직접 따를 수 있는 형태로 변환.

각 단계(red/green/refactor)마다 `description` / `rules` / `must_not` 3필드 (워크북 L800~805 정합).

대표 must_not:
- RED: "테스트 본문에 production 클래스 신규 정의" (import만 허용)
- GREEN: "기존 테스트 변경" (수정·삭제·약화)
- REFACTOR: "새 테스트 추가" (M2 위반)

### 2.5 `testing`

**의도**: pytest 사용 규약 + 테스트 ID 네임스페이스 + 커버리지 임계를 04와 동기화.

핵심 결정:
- `layout`: 5개 서브디렉터리(`tests/entity/`, `boundary/`, `control/`, `data/`, `integration/`) — 04 §5 옵션 (ii) ECB 정렬
- `fixture_scope.default: function` — 테스트 간 상태 누수 방지
- `coverage.targets`: domain 95% / boundary 85% / data 80% / control 90% (04 §4.4 그대로)
- `mocking_policy`: Domain 테스트는 mock 금지, Boundary 테스트는 Domain mock 강제 (04 §2.3 정합)

### 2.6 `forbidden`

**의도**: 9개 금지 패턴. 각각 `pattern` / `reason` / `alternative` 3필드 (워크북 L813~816 정합).

워크북 최소 요구(3개) + 본 프로젝트 추가(6개):

| # | 패턴 | 출처 |
| --- | --- | --- |
| 1 | `print(...)` | 워크북 L817 |
| 2 | `magic number literal 4 or 34 in src/` | 04 §1.2 I5 |
| 3 | `except Exception: pass / bare except:` | 워크북 L817 + 01 §에러와 실패의 분리 |
| 4 | `from X import *` | 04 § |
| 5 | `TODO/FIXME without issue link` | 본 보고서 추가 |
| 6 | `Domain Service에서 Boundary 또는 Control import` | 04 §4.1 |
| 7 | `RED 없이 신규 production 코드` | 02 §3.2 M1 |
| 8 | `테스트의 assert 약화` | 02 §3.2 + 04 §4.3 |
| 9 | `한 PR에서 여러 invariant·단계 혼합` | 02 §2.3 안티패턴 |

### 2.7 `file_structure`

**의도**: 워크북 L818~820의 요구(boundary/, control/, entity/, tests/ 포함)에 맞춰 04 §5 옵션 (ii) ECB 구조를 인코딩.

- `src_tree`: 11개 entity 파일 + 1개 control 파일 + 5개 boundary 파일 (Repository 포함)
- `tests_tree`: 5개 서브디렉터리

각 파일 옆에 보호하는 테스트 ID 주석(예: `# D-LOC-*`) — Cursor가 코드 생성 시 어느 테스트 파일에 영향이 가는지 즉각 파악 가능.

### 2.8 `ai_behavior`

**의도**: 코드 생성 전/중/후 + TDD 위반 감지 + 워크북 단계 완료 시 행동을 명시.

4개 서브섹션:
- `before_writing_code` (4항목): 테스트 존재 확인, ECB 레이어 확인, Traceability 매핑
- `while_writing_code` (4항목): type hints, ECB 경계, literal 금지, docstring
- `after_writing_code` (4항목): RED→GREEN 전환 확인, 전체 pytest, 커버리지, PR 템플릿 요약
- `on_tdd_violation` (감지 신호 3개 + action)
- `on_workbook_step_completion` (3항목): Report+Prompt 페어 산출 등

---

## 3. 검증 — 워크북 L766~772 자기 점검 체크리스트

워크북이 요구한 4가지 자기 검증:

| 항목 | 결과 | 비고 |
| --- | --- | --- |
| 1. YAML 문법 오류 | ✅ Pass | 들여쓰기 2-space, 스칼라/매핑/시퀀스 표기 일관 |
| 2. 누락된 필수 섹션 | ✅ Pass | 8개 최상위 섹션 모두 존재 (`project`, `code_style`, `architecture`, `tdd_rules`, `testing`, `forbidden`, `file_structure`, `ai_behavior`) |
| 3. `tdd_rules`와 `forbidden` 규칙 간 충돌 | ✅ Pass | 양쪽이 "RED 없이 production 코드 금지"를 명시하나 의미가 동일 — 충돌이 아니라 강조 |
| 4. Cursor AI가 실제로 따를 수 없는 `ai_behavior` 규칙 | ⚠️ 주의: `after_writing_code.pytest 실행 확인`은 Cursor 환경에 따라 도구 호출 권한이 필요 — Cursor의 Auto-Run 또는 사용자의 명시적 승인 필요 |

> 항목 4의 제한사항은 **본 보고서에서 명시적으로 알린다**: 본 .cursorrules는 Cursor가 자동으로 `pytest`를 실행할 권한이 없는 환경에서는 "사용자에게 실행을 요청하라"는 의미로 해석되어야 한다.

---

## 4. 동작 확인 가이드 (워크북 L895~908 정렬)

본 `.cursorrules`가 정상 동작하는지 확인하는 절차 — **워크북은 User Entity 작성을 워밍업 예제로 사용**하지만, 본 프로젝트는 다음 워크북 단계(ECB 스켈레톤 + User Entity 워밍업)에서 별도 산출이 예정됨.

지금 단계에서 즉시 확인 가능한 항목:

- [ ] Cursor가 새 파일을 만들 때 `src/entity/`·`src/control/`·`src/boundary/` 경로를 사용하는가
- [ ] Cursor가 함수 시그니처에 type hints를 자동 포함하는가
- [ ] Cursor가 정수 리터럴 `4`·`34`를 `GRID_SIZE`·`MAGIC_CONSTANT`로 대체 제안하는가
- [ ] Cursor가 RED 테스트 없이 production 코드를 제안하면 차단 또는 경고하는가
- [ ] Cursor가 새 워크북 단계 완료 시 Report/Prompt 페어 작성을 제안하는가

> 위 체크리스트는 다음 워크북 단계 진행 중 자연스럽게 검증된다. 별도 일회성 검증은 생략.

---

## 5. 본 규약의 한계 및 진화 경로

### 한계

- `.cursorrules`는 **권고**이지 강제가 아니다 — Cursor·다른 AI가 무시할 수 있다. CI·pre-commit hook으로 보강 필요 (예: `mypy`, `ruff`, `pytest --cov`).
- `forbidden.literal_constants` 규약은 정적 검출이 자체 도구로 보장되지 않음 — `ruff` 또는 자체 lint rule로 보강 권장.
- `ai_behavior.after_writing_code`의 자동 pytest 실행은 환경 의존.

### 진화 경로

| 단계 | 트리거 | 변환 |
| --- | --- | --- |
| 1 | 본 .cursorrules가 5개 이상의 서로 다른 도메인 규약을 가지게 됨 | `.cursor/rules/*.mdc`로 분할 마이그레이션 (예: `architecture.mdc`, `tdd.mdc`, `forbidden.mdc`) |
| 2 | CI 도입 | `forbidden` 규약 일부를 `ruff` rule 또는 custom lint plugin으로 이전 |
| 3 | 팀 협업 진입 | `ai_behavior`에 코드 리뷰 자동 코멘트·PR 체크리스트 검증 항목 추가 |

---

## 6. 다음 단계 진입 조건

본 보고서·`.cursorrules` 머지 후 워크북의 다음 단계는:

> **워크북 §"ECB 폴더 스켈레톤 + User Entity 워밍업"** (L856~917)
> - `src/entity/`·`src/control/`·`src/boundary/` 폴더 생성
> - `src/entity/user.py` 워밍업 (User 엔티티 클래스를 ECB 패턴으로) — `.cursorrules`의 정상 동작 검증 겸용

다만 이 시점부터 **production 코드(Python 파일)가 생성**되므로:

- 02 §2.3 PR 카덴스 적용 시작
- ECB 스켈레톤 자체는 코드 산출이지만 RED 테스트가 없는 워밍업 — `.cursorrules`의 ai_behavior 규약과 충돌. **워밍업은 본 규약의 예외**로 처리하거나, User 워밍업도 RED부터 시작하도록 결정 필요. (다음 단계에서 결정)

---

## 7. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — 워크북 L702~917 8섹션 + 본 프로젝트 추가 결정 8건(ADD-1~8) |

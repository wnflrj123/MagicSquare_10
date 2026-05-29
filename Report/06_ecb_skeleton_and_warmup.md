# 4×4 Magic Square — ECB 스켈레톤 + User 엔티티 워밍업 보고서

> 작성일: 2026-05-29
> 작성 단계: 인프라 부트스트랩 (Infrastructure Bootstrap) — 워크북 §"완성 후 동작 확인" (L895~917) 산출물
> 작업 브랜치: `feature/warmup-user-entity-ecb` → `develop` PR 예정
> 산출물:
> - 인프라: `.gitignore`, `pyproject.toml`
> - ECB 스켈레톤: `src/{entity,control,boundary,boundary/repository}/__init__.py`
> - 워밍업: `tests/entity/test_user.py`, `src/entity/user.py`

---

## 1. 목적

본 단계의 산출은 두 가지를 한꺼번에 수행한다:

1. **`.cursorrules` 동작 검증 (워크북 의도)** — 워크북 L908: "타입힌트가 있고, 파일이 entity/ 폴더에 위치하며, 테스트 파일이 AAA 패턴으로 작성되면 .cursorrules가 정상 동작하는 것"
2. **ECB 디렉터리·Python 인프라 영구 설치** — 후속 모든 RGR 사이클이 의존하는 폴더 구조와 pytest 설정을 develop에 영속

User 엔티티 자체는 **MagicSquare Solver 도메인의 일부가 아니다** — 스모크 테스트용 throwaway 클래스. Solver 코드 진입 후 제거 가능.

---

## 2. 만들어진 것

### 2.1 인프라

| 파일 | 내용 |
| --- | --- |
| `.gitignore` | `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.coverage`, `htmlcov/` |
| `pyproject.toml` | `[project]` 메타 + `[tool.pytest.ini_options]` (testpaths=tests, pythonpath=src, python_files=test_*.py) |

> 이전 `feature/I1-set-equality` 브랜치에 있던 chore 커밋(`b02f7f2`)을 재작성. 동일 내용이지만 본 보고서 §3.2에 따라 develop 라인에 새로 진입.

### 2.2 ECB 스켈레톤 (04 §5 옵션 ii 정합)

```
src/
├── entity/__init__.py            # Domain Layer
├── control/__init__.py           # Use Case Orchestration
└── boundary/
    ├── __init__.py               # 외부 입출력 경계
    └── repository/__init__.py    # Data Adapter (ECB는 Data를 Boundary로 흡수)

tests/
├── entity/                       # D-* 테스트
├── control/                      # 컨트롤 테스트
├── boundary/                     # U-* 테스트
├── data/                         # DAT-* 테스트
└── integration/                  # I-INT-* 테스트
```

`tests/*` 서브디렉터리는 빈 상태로 워킹 트리에만 존재한다 (Git은 빈 디렉터리를 추적하지 않음). 각 디렉터리의 첫 테스트 파일이 들어가는 순간 자동 추적된다.

### 2.3 워밍업 — User 엔티티 RGR 1사이클

| 단계 | 커밋 | 내용 |
| --- | --- | --- |
| 🔴 RED | `0b9001d` | `tests/entity/test_user.py` — `test_user_creation_stores_id_name_email` (AAA, Google docstring, type hints) |
| 🟢 GREEN | `6578352` | `src/entity/user.py` — `@dataclass(frozen=True) User(id, name, email)` |
| 🔵 REFACTOR | (skip) | 구조 개선 여지 없음 — 정직한 skip |

---

## 3. .cursorrules 동작 검증

워크북 L908의 통과 기준 4개를 본 워밍업이 모두 충족:

| 기준 | 결과 | 증거 |
| --- | --- | --- |
| 타입힌트가 있다 | ✅ | `User` 모든 필드에 `str` annotation |
| 파일이 `entity/` 폴더에 위치 | ✅ | `src/entity/user.py` |
| 테스트 파일이 AAA 패턴 | ✅ | `test_user.py` 본문에 `# Arrange`·`# Act`·`# Assert` 주석 + 코드 3블록 |
| Google docstring | ✅ | 모듈·클래스 모두 `"""..."""` + `Args:` 섹션 |

추가로 .cursorrules가 강제하는 다른 규약도 충족:

| .cursorrules 규약 | 충족 여부 |
| --- | --- |
| `architecture.layers.entity.path: src/entity/` | ✅ |
| `code_style.max_line_length: 88` | ✅ (최장 줄 ~70자) |
| `code_style.literal_constants.forbidden_literals_in_src: [4, 34]` | ✅ (해당 없음) |
| `tdd_rules.red_phase.rules`: 테스트 먼저, AAA 3단락, production 코드 미포함 | ✅ (RED 커밋에 src/ 변경 0건) |
| `tdd_rules.green_phase.rules`: 최소 변경, 리팩토 금지 | ✅ (User dataclass 외 추가 로직 0건) |
| `forbidden.RED 없이 신규 production 코드` | ✅ (RED → GREEN 순서 보존) |

> 본 워밍업의 가장 큰 가치는 **`.cursorrules`와 우리 TDD 규약이 충돌 없이 양립한다는 사실의 증명**이다 — 05 §3 자기 검증의 항목 3(tdd_rules ↔ forbidden 충돌 없음)이 실제 코드 생성에서도 유지됨.

---

## 4. PR 결정 (02 §2.3 적용)

본 변경은 production 코드를 처음으로 도입한다. 02 §2.3 카덴스 매핑:

| 카덴스 | 조건 | 본 PR |
| --- | --- | --- |
| A1 (RED 테스트 플랜 완성) | `tests/` 의 RED skeleton 완성 | △ 워밍업 1건뿐. 본 PR은 A1 + A2 통합 |
| A2 (GREEN 완성) | 모든 RED가 GREEN으로 전환 | ✅ 1/1 GREEN |
| A3 (REFACTOR 완성) | 구조 개선 + 동작 보존 | (skip — 구조 개선 여지 없음) |
| B1 (release 머지) | 마일스톤 도달 + 문서 동기화 | ❌ (B1 단계 아님) |

→ **feature → develop PR을 만든다** (A1+A2 결합). 머지 후 develop은 워크북의 "ECB 스켈레톤 + 워밍업" 단계를 완료한 상태가 된다.

---

## 5. 본 단계의 한계 및 다음 단계

### 한계

- **User 엔티티는 throwaway** — Solver 도메인 시작 시 제거 또는 무시 가능.
- **검증 로직 없음** — id 비어 있음, 이메일 형식 등 검증은 의도적으로 미루었다 (워크북은 워밍업에서 검증을 요구하지 않음).
- **`.cursorrules` 자동 lint 미도입** — `ruff`·`mypy` 같은 정적 분석 도구가 없으므로 규약 위반은 사람이 잡아야 한다. 본 워밍업은 사람(AI)이 직접 규약 충족을 확인한 사례.

### 다음 단계 (워크북 기준)

머지 후 워크북의 다음 단계:

1. **Skills 등록** (`.cursor/skills/magic-square-tdd/`) — 워크북 L1356~. Agent용 재사용 설명서 작성.
2. **Agent 프롬프트 세트** (8개 역할) — 워크북 L1574~.
3. **P-01 User Journey** (Epic → Story → AC → Scenario) — 워크북 L1690~.
4. **P-02 PRD** (Gherkin 포함) — 워크북 L2596~.

→ 본격적인 Solver 도메인 RGR은 P-02 이후 (테스트 플랜 + RED Skeleton 단계, 워크북 L3876).

---

## 6. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — ECB 스켈레톤 + 인프라 + User 워밍업 (워크북 L856~917) |

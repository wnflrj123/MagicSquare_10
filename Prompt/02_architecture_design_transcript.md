# Prompt Transcript — 4×4 Magic Square 아키텍처·테스트·통합 설계 세션

> 내보낸 날짜: 2026-05-29
> 브랜치: develop
> 세션 주제: 워크북 §과제 1 "아키텍처/테스트/통합 요청 프롬프트 작성" 실행
> 형식: 워크북 프롬프트 (verbatim) + 어시스턴트 응답 요약 + 산출물 매핑
> 산출물: [`Report/04_architecture_design.md`](../Report/04_architecture_design.md)

---

## 📌 세션 컨텍스트

- 작업 디렉토리: `/Users/juri/Projects/sec_cursor/MagicSquare_1130`
- 출처 문서: `../CursorAI/응용-...실습-워크 북.docx` (L591~720)
- 직전 산출물:
  - [`Report/01_problem_definition.md`](../Report/01_problem_definition.md) v2.0 (2026-05-29 Solver 정렬)
  - [`Report/02_branching_strategy.md`](../Report/02_branching_strategy.md)
  - ~~`Report/03_prd.md`~~ — SUPERSEDED
- 본 세션 산출물:
  - [`Report/04_architecture_design.md`](../Report/04_architecture_design.md) (Logic/Screen/Data/Integration 4계층 설계 + Traceability Matrix)
  - 본 전사본

---

## 1️⃣ 워크북 §과제 1 — Cursor 권장 프롬프트 생성 패턴

워크북 L593~596은 직접 긴 프롬프트를 작성하는 대신 다음 4단계를 권장한다:

> 1단계: Cursor에게 "좋은 과제 프롬프트를 만들어 달라"고 요청
> 2단계: Cursor가 만든 프롬프트를 검토
> 3단계: 그 프롬프트를 다시 Cursor에 실행
> 4단계: 산출물 생성

본 프로젝트는 워크북이 이미 1~2단계의 산출물을 제공하므로 (L611~691에 완성된 프롬프트가 있음), **3단계부터 시작**한다.

---

## 2️⃣ 워크북 프롬프트 (verbatim, L611~691)

```
당신은 Dual-Track UI + Logic TDD 및 Clean Architecture 설계 전문가입니다.
프로젝트: Magic Square (4x4) — TDD 연습용
목적: 알고리즘 난이도보다 "레이어 분리 + 계약 기반 테스트 + 리팩토링" 훈련

제약:
- 구현 코드는 작성하지 마십시오. (설계/계약/테스트/통합 계획만)
- UI는 실제 화면이 아니라 "입력/출력 경계(Boundary)"로 정의
- Data Layer는 DB가 아니라 "저장/로드 인터페이스(메모리/파일 교체 가능)" 수준만
- 입력/출력은 명확히 고정

입력 계약:
- 4x4 int[][] (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지

출력 계약:
- int[6]
- 좌표는 1-index
- 반환 형식: [r1,c1,n1,r2,c2,n2]
- n1,n2는 두 누락 숫자이며, (작은수→첫빈칸, 큰수→둘째빈칸) 조합이 마방진이면
  그 순서로, 아니면 반대

------------------------------------------------------------
출력 형식 (반드시 이 구조로)
------------------------------------------------------------
# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
- Entities / Value Objects / Domain Services 목록과 책임(SRP)
## 1.2 도메인 불변조건(Invariants)
- 행/열/대각선 합 일치, Magic Constant 등
## 1.3 핵심 유스케이스(도메인 관점)
- 빈칸 찾기, 누락 숫자 찾기, 마방진 판정, 두 조합 시도
## 1.4 Domain API(내부 계약)
- 메서드 시그니처 수준(코드 X) + 입력/출력/실패조건
## 1.5 Domain 단위 테스트 설계(RED 우선)
- 테스트 케이스 목록(정상/비정상/엣지)
- 각 테스트가 보호하는 invariant 명시

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
- "행렬 입력 → 검증 → 결과 출력" 흐름
## 2.2 UI 계약(외부 계약)
- Input schema / Output schema / Error schema
## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
- 잘못된 크기, 빈칸 개수 오류, 값 범위 오류, 중복 오류, 반환 포맷 검증
- Domain은 Mock으로 가정
## 2.4 UX/출력 규칙
- 에러 메시지 표준(정확한 문구 규칙까지)

# 3) Data Layer 설계 (Data Layer)
## 3.1 목적 정의
- "저장/로드"의 필요성과 범위(학습용)
## 3.2 인터페이스 계약
- 예: MatrixRepository.save/load (메서드 수준, 코드 X)
- 저장 대상: 입력 행렬, 실행 결과(선택)
## 3.3 구현 옵션 비교(메모리/파일)
- 옵션 A: InMemory / 옵션 B: File(JSON/CSV)
- 추천안 1개 선택 + 이유
## 3.4 Data 레이어 테스트
- 저장/로드 정합성, 예외(파일 없음/형식 오류), 불변조건(4x4 유지)

# 4) Integration & Verification (통합 및 검증)
## 4.1 통합 경로 정의
- UI → Application(선택) → Domain → Data 흐름(의존성 방향 포함)
## 4.2 통합 테스트 시나리오
- 정상 시나리오 2개 이상
- 실패 시나리오 3개 이상(입력 오류, 도메인 실패, 데이터 실패)
## 4.3 회귀 보호 규칙
- 기존 테스트 유지 정책
- 변경 금지 규칙(계약/출력 포맷)
## 4.4 커버리지 목표
- Domain Logic 95%+
- UI Boundary 85%+
- Data 80%+
## 4.5 Traceability Matrix (필수)
- Concept(Invariant) → Rule → Use Case → Contract → Test → Component

------------------------------------------------------------
추가 조건
------------------------------------------------------------
- 모호한 표현 금지("적절히/충분히" 금지)
- 모든 규칙은 검증 가능해야 함(테스트로 확인 가능)
- 구현 코드 작성 금지
- 표/체크리스트를 적극 사용
```

추가 사용자 지시 (워크북 L697~699):

> 다음의 순서로 실행해줘
> 1. Report 폴더에 보고서 생성해줘
> 2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘

---

## 3️⃣ 어시스턴트 응답 요약

### 입력 분석
- 워크북 프롬프트는 도메인 = **Solver** (빈칸 2개의 4×4 → int[6])이며, 이는 본 프로젝트의 `01_problem_definition.md` v2.0 (2026-05-29 Solver 정렬)과 일치.
- 따라서 워크북 프롬프트와 우리 보고서의 invariant 체계(I1~I12)·에러 코드 체계(E001~E005)를 **양방향 매핑**하여 한 산출물에 통합 가능.
- 폴더 구조는 워크북이 후속 단계에서 **ECB 명명**(Entity/Control/Boundary)을 채택할 것으로 보여 옵션 (ii) ECB를 추천으로 표기.

### 산출 구조
워크북이 요구한 4섹션 + 본 프로젝트 컨텍스트가 요구하는 2섹션을 추가:

| § | 제목 | 워크북 요구 | 추가 사유 |
| --- | --- | --- | --- |
| 0 | 본 보고서의 약속 | — | 명명 규칙·테스트 ID 체계를 한 곳에 못박음 (모호함 방지) |
| 1 | Logic Layer 설계 | ✅ | 워크북 요구 그대로 |
| 2 | Screen Layer (Boundary) 설계 | ✅ | 워크북 요구 그대로 |
| 3 | Data Layer 설계 | ✅ | 워크북 요구 그대로 |
| 4 | Integration & Verification | ✅ | 워크북 요구 그대로 |
| 5 | 컴포넌트 폴더 구조 | — | 워크북 후속 단계가 폴더 구조를 가정하므로 사전 결정 |
| 6 | 다음 단계 진입 조건 (DoR) | — | P-02(PRD)로 넘어가기 위한 체크리스트 |
| 7 | 의도적으로 미루는 결정 | — | 본 보고서가 결정하지 **않는** 것을 명시 |
| 8 | 변경 이력 | — | 표준 |

### 핵심 설계 결정 (본 세션에서 단독으로 정한 것)

| # | 결정 | 사유 |
| --- | --- | --- |
| D-1 | 테스트 ID 네임스페이스를 `D-*` / `U-*` / `DAT-*` / `I-INT-*` 4종으로 분리 | 워크북 후속 단계와 호환 |
| D-2 | 에러 코드 `E001~E005` 5종으로 확정 (E001 INVALID_SIZE ~ E005 NO_VALID_MAGIC_SQUARE) | 워크북이 `INVALID_SIZE`, `NO_VALID_MAGIC_SQUARE` 명을 직접 사용. 우리 invariant I1~I4(입력)·I11(실패)에 1:1 매핑 |
| D-3 | Data Layer 구현은 **InMemory 우선 → File 후속** | MVP 단순성 + Golden Master 단계에서 File 필요 |
| D-4 | 폴더 구조는 **ECB** (옵션 ii) 추천, Clean Architecture 4분할(옵션 i)도 병기 | 워크북 후속이 ECB 사용 |
| D-5 | "정확한 에러 메시지 문구"는 본 보고서가 결정하지 않음 (§7) | P-02 PRD에서 확정될 것 |
| D-6 | Repository는 Boundary 하위(`boundary/repository/`)에 두는 ECB 흡수 채택 | 워크북 ECB 관행 |

### 매핑 검증
- `01_problem_definition.md` v2.0의 I1~I12 12개 invariant 모두 §4.5 Traceability Matrix에 등재됨 (12행).
- 각 invariant마다 최소 1개의 테스트 ID가 매핑됨 (D-VAL-07 정적 분석 포함).
- 모든 에러 코드 E001~E005가 §2.2에 정의되고 §4.5의 Contract 열에 매핑됨.

---

## 4️⃣ 산출물 인덱스

| # | 파일 | 역할 |
| --- | --- | --- |
| 1 | `Report/01_problem_definition.md` v2.0 | 문제 정의 (Solver 도메인) |
| 2 | `Report/02_branching_strategy.md` | 브랜치·커밋 전략 |
| 3 | `Report/03_prd.md` | ⚠️ SUPERSEDED (학습 기록 보존) |
| 4 | `Report/04_architecture_design.md` | **본 세션 산출** — 4계층 설계 + Traceability |
| 5 | `Prompt/01_problem_definition_transcript.md` | 01 작성 세션 전사 |
| 6 | `Prompt/02_architecture_design_transcript.md` | **본 세션 전사** |

---

## 5️⃣ 다음 단계 (워크북 기준)

본 산출물 머지 후 워크북의 후속 절차:

1. **Cursor Rules 작성** (`.cursorrules`) — 워크북 L708~ (Python 3.10+, PEP8, type hints, pytest+AAA, ECB, Dual-Track TDD, print 디버깅 금지 등 인코딩)
2. **ECB 폴더 스켈레톤 + User Entity 워밍업** — 워크북 L856~
3. **Skills 등록** (`.cursor/skills/magic-square-tdd/`) — 워크북 L1356~
4. **Agent 프롬프트 세트** (8개 역할) — 워크북 L1574~
5. **P-01 User Journey** (Epic → Story → AC → Scenario) — 워크북 L1690~
6. **P-02 PRD** (Gherkin 포함, `docs/PRD_MagicSquare.md`) — 워크북 L2596~. 본 04 보고서의 §6 DoR 체크리스트가 입력이 됨
7. **P-03 To-Do 리스트**·README 갱신 — 워크북 L3316·L3531
8. **테스트 플랜 + RED Skeleton** — 워크북 L3876
9. **P-06 GREEN** — 단일 커밋 최소 구현 — 워크북 L4525
10. **Golden Master 자동화 + REFACTOR** — 워크북 L5048·L5552

---

## 🔖 메모

- 본 전사본은 워크북 프롬프트(verbatim) + 어시스턴트 응답 요약 형식으로 보존. 어시스턴트의 전체 응답은 `Report/04_architecture_design.md`에 직접 저장되어 있으므로 중복하지 않음.
- 본 세션의 사용자 트리거는 단 두 글자("고고")였으나, 직전 대화에서 다음 단계가 명확히 합의되어 있었음 (Solver 정렬 + 04 작성 + 02 전사본 페어).

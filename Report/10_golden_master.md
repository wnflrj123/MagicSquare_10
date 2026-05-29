# Golden Master 회귀 잠금 보고서 (M6 / I-GM-01)

> 작성일: 2026-05-29
> 단계: M6 (Golden Master) — 워크북 §"GM — Golden Master 자동화" (L5048~5276) 산출물
> 산출 파일:
> - `tests/golden_master/test_gm_01_magic_square_golden_master.py` (테스트)
> - `tests/golden_master/golden_master_expected.json` (baseline, 8건)
> - `tests/conftest.py` (`--approve-golden` CLI 옵션)
> 전제 문서: PRD `Report/08_prd.md` §11 L7, 아키텍처 `Report/04` §4.2 I-GM-01

---

## 1. Golden Master 회귀 잠금이란 (Magic Square 맥락)

### 정의

**Approval/Golden Master testing**: 시스템의 현재 출력을 "정답(baseline)"으로 한 번 기록해 두고, 이후 모든 실행에서 그 baseline과 정확히 일치하는지를 검증하는 회귀 방어 패턴.

### 본 프로젝트에서의 역할

| 항목 | 본 프로젝트 |
| --- | --- |
| baseline 단위 | `int[6]` 결과 + 에러 `(code, type, message)` |
| 비교 단위 | 8건 입력에 대한 `SolveBoundary.solve()` 출력 (JSON 직렬화) |
| 활성화 시점 | 본 보고서 머지 후 |
| 회귀 검출 대상 | I10 (int[6] 구조)·E001~E005 정문구·Step A/B 결정성 |

### 단위 테스트와의 차이

| | 단위 테스트 (D-*, U-*, I-INT-*) | Golden Master (I-GM-01) |
| --- | --- | --- |
| 검증 대상 | "각 invariant가 지켜지는가" | "전체 시스템 출력이 baseline과 비트 단위로 같은가" |
| 변경 감지 | 의도 명확한 위반만 | **의도하지 않은 모든 출력 변화** |
| 갱신 방법 | 코드 수정 → 테스트 PASS | `--approve-golden` 명시 + baseline 파일 갱신 PR |
| 잠금 강도 | 약 (어설션 통과면 OK) | 강 (1바이트만 달라도 fail) |

> **본질**: 단위 테스트가 "내가 정의한 invariant"를 보호한다면, Golden Master는 "내가 정의하지 않았지만 현재 동작하는 모든 것"을 보호한다.

---

## 2. 케이스 매트릭스 (8건)

| ID | 시나리오 | 입력 요지 | 기대 출력 |
| --- | --- | --- | --- |
| GM-TC-01 | Step A 성공 | Dürer에서 (1,3)·(3,1) 가림 | `{"ok": true, "value": [1,3,2,3,1,9]}` |
| GM-TC-02 | Step B reverse 성공 | Dürer에서 (1,1)·(4,4) 가림 | `{"ok": true, "value": [1,1,16,4,4,1]}` |
| GM-TC-03 | 풀 수 없음 | Step A·B 모두 실패 입력 | `E005 NO_VALID_MAGIC_SQUARE` |
| GM-TC-04 | I1 위반 | 3×4 행렬 | `E001 INVALID_SIZE` "Grid must be 4x4." |
| GM-TC-05 | I2 위반 | 빈칸 0개 (Dürer 완성형) | `E002 INVALID_BLANK_COUNT` |
| GM-TC-06 | I3 위반 (음수) | -1 포함 | `E003 INVALID_VALUE_RANGE` |
| GM-TC-07 | I3 위반 (17) | 17 포함 | `E003 INVALID_VALUE_RANGE` |
| GM-TC-08 | I4 위반 | 5 중복 | `E004 DUPLICATE_VALUE` |

8건이 본 프로젝트의 **공개 출력 API의 모든 분기**를 커버한다 (성공 2종·도메인 실패 1종·입력 에러 5종).

---

## 3. 운영 명령

### 일상 (회귀 검출)

```bash
.venv/bin/python -m pytest tests/golden_master/ -v
# 또는 전체 스위트 일부로 자동 실행
.venv/bin/python -m pytest -v
```

baseline과 일치하면 PASS, 1바이트라도 다르면 FAIL.

### 의도된 변경 시 (baseline 갱신)

```bash
.venv/bin/python -m pytest tests/golden_master/ --approve-golden -v
```

→ 현재 `SolveBoundary` 출력을 baseline에 덮어쓴 뒤 SKIP 표시.
→ 갱신된 `golden_master_expected.json`을 **별도 PR로 머지** (코드 변경 PR과 분리하여 reviewer가 diff를 명확히 검토).

### baseline 미존재 (최초 또는 삭제 후)

테스트가 `pytest.fail`로 명시적 안내 → 위 `--approve-golden` 명령으로 재생성.

---

## 4. 회귀 발생 시 의사결정 흐름

```
GM 테스트 FAIL
  │
  ▼
diff 확인 (golden_master_expected.json vs 실제 출력)
  │
  ├── (A) 의도하지 않은 변화 (회귀)
  │       → production 코드 수정으로 baseline 복원
  │       → GM 테스트 다시 PASS
  │
  └── (B) 의도한 변화 (예: 에러 메시지 개선, int[6] 외 정보 추가)
          → 별도 PR
              1) production 변경 (단위 테스트도 같이 갱신)
              2) `--approve-golden`으로 baseline 갱신
              3) PR 본문에 "어떤 의도로 baseline이 어떻게 달라졌는지" 명시
              4) 리뷰어가 diff 검토 후 머지
```

> **금기 안티패턴**: 의도하지 않은 변경에 대해 `--approve-golden`으로 즉시 baseline을 갱신하지 말 것 — 회귀를 정상화로 위장하는 행위.

---

## 5. 잠금되는 항목 (현 baseline 기준)

본 baseline이 활성화된 이후 **다음 변경은 즉시 GM fail**:

| 변경 | 영향 받는 케이스 |
| --- | --- |
| `int[6]` 출력 형식 변경 (예: 길이·순서·index 기준 변경) | GM-TC-01, GM-TC-02 |
| Step A·B 우선순위 뒤집힘 | GM-TC-01, GM-TC-02 |
| 에러 코드 식별자 변경 (E001~E005) | GM-TC-03~08 |
| 에러 정문구 메시지 변경 (단 한 글자라도) | GM-TC-03~08 |
| 에러 `type` 분류 변경 (INPUT_ERROR ↔ DOMAIN_FAILURE) | GM-TC-03~08 |
| `MAGIC_CONSTANT`·`GRID_SIZE` 값 변경 | 전체 |
| 입력 검증 순서 변경으로 동일 입력에 다른 에러 코드 반환 | GM-TC-06, GM-TC-07, GM-TC-08 (잠재적) |

즉 PRD §11 회귀 잠금 표의 **L1·L2·L3·L4·L5·L6 모두**가 GM-TC-01~08 단일 파일로 통합 검증된다.

---

## 6. 본 산출물의 한계

- **baseline은 "현재 동작 = 정답" 가정**이라, 현재 동작에 잠재 버그가 있어도 그대로 잠긴다. 본 baseline 활성화 전 단위 테스트(58건) 통과로 정합성을 확보했으나, 단위 테스트가 못 보는 영역은 GM도 못 본다.
- **8건은 분기 커버이지 입력 공간 커버는 아니다.** 모든 4×4 부분 마방진 (∼16!/14! 조합)을 검증하는 게 아님. 후속에서 property-based testing(예: hypothesis) 도입 검토 가능.
- **시각(GUI) 동작은 잠그지 않는다.** GM은 `SolveBoundary` 출력만. GUI 표시 형식 회귀는 별도 G-UI-* 테스트가 담당.

---

## 7. 다음 단계 (Refactor Cycle)

본 GM 머지 후, Refactor Cycle (`refactor/refactor` 브랜치) 진입 가능:

1. `refactor/refactor` 브랜치 생성
2. 동작 보존 구조 개선 (예: Domain Service들에서 중복 격자 순회 최적화, 상수 추출 등)
3. 매 변경 후 `pytest -v` → 59/59 GREEN + GM matched 확인
4. A3 카덴스 PR로 develop 머지

> Refactor 단계의 "동작 보존" 약속이 본 GM에 의해 **기계적으로 검증**된다.

---

## 8. 변경 이력

| 일자 | 버전 | 변경 |
| --- | --- | --- |
| 2026-05-29 | v1.0 | 초판 — 8건 baseline 정착, --approve-golden 옵션 |

"""G-UI-* — MagicSquareMainWindow 스모크 테스트.

GUI 위젯 구조 + boundary 주입 + 풀기 핸들러 동작을 offscreen 플랫폼으로 검증.
실제 시각 검증은 `python -m boundary.screen.app` 수동 실행으로.

PRD `Report/08_prd.md` §9.2 GUI MainWindow 정합.
"""
from __future__ import annotations

import os

# offscreen 플랫폼 강제 — display 없는 환경(CI)에서도 동작
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from typing import Any, List

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication

from boundary.error_codes import ErrorCode
from boundary.screen.app import WINDOW_TITLE, MagicSquareMainWindow


@pytest.fixture(scope="module")
def qapp() -> QApplication:
    """모듈 단일 QApplication 인스턴스 (PyQt 요구사항)."""
    app = QApplication.instance() or QApplication([])
    return app


def _set_grid(window: MagicSquareMainWindow, grid: List[List[int]]) -> None:
    """테스트용 헬퍼 — SpinBox 값을 격자로 일괄 설정."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            window.spinboxes[r][c].setValue(value)


def test_window_title_g_ui_01(qapp: QApplication) -> None:
    """G-UI-01 — 창 제목은 PRD §9.2 명시값."""
    window = MagicSquareMainWindow()
    assert window.windowTitle() == WINDOW_TITLE
    assert WINDOW_TITLE == "Magic Square 4x4"


def test_window_has_4x4_spinboxes_g_ui_02(qapp: QApplication) -> None:
    """G-UI-02 — 4×4 SpinBox 격자가 구성됨, 각 SpinBox 범위 [0, 16]."""
    window = MagicSquareMainWindow()
    assert len(window.spinboxes) == 4
    assert all(len(row) == 4 for row in window.spinboxes)
    for row in window.spinboxes:
        for spin in row:
            assert spin.minimum() == 0
            assert spin.maximum() == 16


def test_solve_with_step_a_success_displays_int6_g_ui_03(
    qapp: QApplication, partial_step_a_grid: List[List[int]]
) -> None:
    """G-UI-03 — Step A 성공 입력 → 결과 영역에 int[6] 표시."""
    window = MagicSquareMainWindow()
    _set_grid(window, partial_step_a_grid)

    window._on_solve_clicked()

    text = window.result_display.toPlainText()
    assert "int[6] = [1, 3, 2, 3, 1, 9]" in text
    assert "완성된 격자" in text


def test_solve_with_unsolvable_displays_e005_g_ui_04(
    qapp: QApplication, unsolvable_grid: List[List[int]]
) -> None:
    """G-UI-04 — 풀 수 없는 입력 → E005 에러 코드 + 정문구 표시."""
    window = MagicSquareMainWindow()
    _set_grid(window, unsolvable_grid)

    window._on_solve_clicked()

    text = window.result_display.toPlainText()
    assert ErrorCode.NO_VALID_MAGIC_SQUARE.value in text  # "E005"
    assert "No valid magic square found." in text


def test_solve_with_invalid_blank_count_displays_e002_g_ui_05(
    qapp: QApplication, durer_grid: List[List[int]]
) -> None:
    """G-UI-05 — 빈칸 0개(완성형) 입력 → E002 표시 (Boundary 검증 차단)."""
    window = MagicSquareMainWindow()
    _set_grid(window, durer_grid)  # 빈칸 없음

    window._on_solve_clicked()

    text = window.result_display.toPlainText()
    assert ErrorCode.INVALID_BLANK_COUNT.value in text  # "E002"


def test_boundary_injection_uses_provided_object_g_ui_06(qapp: QApplication) -> None:
    """G-UI-06 — boundary 주입 시 기본 composition 대신 주입된 객체 사용."""
    from unittest.mock import MagicMock

    fake_boundary = MagicMock()
    window = MagicSquareMainWindow(boundary=fake_boundary)

    assert window.boundary is fake_boundary


def test_spinbox_selects_all_on_focus_g_ui_07(qapp: QApplication) -> None:
    """G-UI-07 — SpinBox 포커스 시 기존 텍스트가 모두 선택되어 키 입력이 덮어쓴다.

    QSpinBox 기본 동작은 포커스 시 텍스트 미선택 → 키 입력이 append 됨.
    이 동작은 '2 → 0 입력' 의도가 '20 → MAX_VALUE clamp'로 잘못 처리되는 원인.
    본 테스트는 focusInEvent 핸들러를 직접 호출해 selectAll 동작을 검증
    (offscreen 환경에서 setFocus는 신뢰성 떨어짐).
    """
    from PyQt6.QtCore import QEvent, Qt
    from PyQt6.QtGui import QFocusEvent

    window = MagicSquareMainWindow()
    spin = window.spinboxes[0][0]
    spin.setValue(5)

    # Act — focusInEvent 직접 호출 (override가 selectAll을 부르도록)
    spin.focusInEvent(
        QFocusEvent(QEvent.Type.FocusIn, Qt.FocusReason.MouseFocusReason)
    )

    # Assert — 모든 텍스트가 선택된 상태
    line_edit = spin.lineEdit()
    assert line_edit.hasSelectedText() is True
    assert line_edit.selectedText() == "5"

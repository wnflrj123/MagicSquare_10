"""PyQt6 GUI for Magic Square 4×4 Partial Solver.

PRD `Report/08_prd.md` §9.2 GUI MainWindow 명세 정합.
워크북 L4987~5024 정합.

실행:
    .venv/bin/python -m boundary.screen.app

Composition root: `MagicSquareMainWindow()`가 기본값으로 SolveBoundary +
SolvePartialMagicSquare 를 주입한다. 테스트에서는 mock boundary 주입 가능.
"""
from __future__ import annotations

import sys
from typing import Any, List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFocusEvent
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SelectAllSpinBox(QSpinBox):
    """QSpinBox 포커스 시 텍스트 전체 선택 → 키 입력이 기존 값을 덮어쓰도록.

    QSpinBox 기본 동작은 포커스 시 텍스트 미선택이라, 값 2인 칸에 '0' 키 입력 시
    '20' → MAX_VALUE clamp 동작으로 사용자 의도(0으로 변경)를 충족하지 못함.
    본 클래스는 G-UI-07 통과를 위해 focusInEvent를 오버라이드한다.
    """

    def focusInEvent(self, event: QFocusEvent) -> None:
        """포커스 진입 직후 selectAll로 전체 텍스트 선택 상태로 만든다.

        Qt의 기본 focusInEvent는 selectAll을 수행하지 않아 키 입력이 append 됨.
        본 오버라이드는 super().focusInEvent 완료 직후 동기적으로 selectAll 호출.
        """
        super().focusInEvent(event)
        self.selectAll()

from boundary.error_codes import ErrorObject, Result
from boundary.solve_boundary import SolveBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare
from entity.constants import BLANK_VALUE, GRID_SIZE, MAX_VALUE


WINDOW_TITLE: str = "Magic Square 4x4"


class MagicSquareMainWindow(QMainWindow):
    """4×4 부분 마방진 입력 → 풀기 → 결과 표시 메인 윈도우."""

    def __init__(self, boundary: Optional[Any] = None) -> None:
        """메인 윈도우 생성.

        Args:
            boundary: SolveBoundary 또는 호환 객체. 기본값은 기본 composition.
        """
        super().__init__()
        self.boundary: Any = boundary or SolveBoundary(
            use_case=SolvePartialMagicSquare()
        )
        self.setWindowTitle(WINDOW_TITLE)
        self.spinboxes: List[List[QSpinBox]] = []
        self.result_display: QTextEdit = QTextEdit()
        self._build_ui()

    def _build_ui(self) -> None:
        """위젯 트리 구성: 4×4 격자 + 풀기 버튼 + 결과 영역."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 4×4 SpinBox 격자
        grid_layout = QGridLayout()
        for row_index in range(GRID_SIZE):
            row_boxes: List[QSpinBox] = []
            for col_index in range(GRID_SIZE):
                spin = SelectAllSpinBox()
                spin.setRange(BLANK_VALUE, MAX_VALUE)
                spin.setValue(BLANK_VALUE)
                spin.setMinimumWidth(60)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid_layout.addWidget(spin, row_index, col_index)
                row_boxes.append(spin)
            self.spinboxes.append(row_boxes)
        layout.addLayout(grid_layout)

        # 풀기 버튼
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        layout.addWidget(solve_button)

        # 결과 라벨 + 영역
        layout.addWidget(QLabel("결과:"))
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(180)
        layout.addWidget(self.result_display)

    def _read_grid(self) -> List[List[int]]:
        """현재 SpinBox 값들을 4×4 격자로 반환."""
        return [[spin.value() for spin in row] for row in self.spinboxes]

    def _on_solve_clicked(self) -> None:
        """'풀기' 클릭 핸들러 — Boundary 호출 후 결과 표시."""
        grid = self._read_grid()
        result: Result = self.boundary.solve(grid)
        if result.is_ok:
            self._display_success(grid, result.value or [])
        elif result.error is not None:
            self._display_error(result.error)

    def _display_success(self, original: List[List[int]], int6: List[int]) -> None:
        """성공 — int[6] + 완성 격자를 결과 영역에 표시."""
        completed = [row[:] for row in original]
        r1, c1, n1, r2, c2, n2 = int6
        completed[r1 - 1][c1 - 1] = n1
        completed[r2 - 1][c2 - 1] = n2

        lines: List[str] = [
            f"✅ Magic square 완성",
            f"int[6] = {int6}",
            "",
            "완성된 격자:",
        ]
        for row in completed:
            lines.append("  " + "  ".join(f"{v:2d}" for v in row))
        self.result_display.setPlainText("\n".join(lines))

    def _display_error(self, error: ErrorObject) -> None:
        """실패 — 에러 코드 + 정문구 메시지 표시."""
        self.result_display.setPlainText(
            f"❌ {error.code.value} ({error.type})\n{error.message}"
        )


def main() -> int:
    """CLI entry point.

    Returns:
        QApplication.exec() 반환 코드.
    """
    app = QApplication(sys.argv)
    window = MagicSquareMainWindow()
    window.resize(420, 480)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

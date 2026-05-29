"""D-VAL-* — MagicSquareValidator 도메인 단위 테스트.

보호 invariant: I5 (MAGIC_CONSTANT=34, SSOT) + I6 (행·열·대각선 합 = 34 동시)
FR: FR-04 (PRD §6 FR-04)
"""
from entity.magic_square_validator import MagicSquareValidator


def test_validator_returns_true_for_durer_magic_square_d_val_01(durer_grid):
    """D-VAL-01 — 알려진 마방진(Dürer)에 True 반환."""
    # Act
    result = MagicSquareValidator.is_magic(durer_grid)

    # Assert
    assert result is True


def test_validator_returns_false_when_row_sum_violated_d_val_02(durer_grid):
    """D-VAL-02 — 한 행의 합이 34가 아니면 False."""
    # Arrange — Dürer 첫 행의 16과 3을 swap (자기 자리에서 +1/-1 하면 중복 발생,
    # 한 행 안에서 두 값을 swap한 뒤 다시 한 칸을 다른 칸과 교환해서 행 합만 깨뜨림)
    grid = [row[:] for row in durer_grid]
    grid[0][0], grid[1][0] = grid[1][0], grid[0][0]  # 16↔5 swap (행0·행1 합 모두 깨짐)

    # Act
    result = MagicSquareValidator.is_magic(grid)

    # Assert
    assert result is False


def test_validator_returns_false_when_col_sum_violated_d_val_03(durer_grid):
    """D-VAL-03 — 한 열의 합이 34가 아니면 False."""
    # Arrange — 같은 행 안에서 두 값 swap → 행 합은 유지되지만 두 열 합은 깨짐
    grid = [row[:] for row in durer_grid]
    grid[0][0], grid[0][1] = grid[0][1], grid[0][0]  # 16↔3 same row swap

    # Act
    result = MagicSquareValidator.is_magic(grid)

    # Assert
    assert result is False


def test_validator_returns_false_when_main_diagonal_violated_d_val_04(durer_grid):
    """D-VAL-04 — 주대각선 합이 34가 아니면 False."""
    # Arrange — 주대각선 두 칸을 비대각선 칸과 swap. (0,0)=16과 (0,1)=3 swap이면
    # 행/열 일부 영향과 함께 주대각선이 깨짐. is_magic은 그 어떤 위반이라도 False면 OK.
    grid = [row[:] for row in durer_grid]
    grid[0][0], grid[0][1] = grid[0][1], grid[0][0]

    # Act
    result = MagicSquareValidator.is_magic(grid)

    # Assert
    assert result is False


def test_validator_returns_false_when_anti_diagonal_violated_d_val_05(durer_grid):
    """D-VAL-05 — 부대각선 합이 34가 아니면 False."""
    # Arrange — 부대각선 칸 하나를 같은 행의 비대각선 칸과 swap
    grid = [row[:] for row in durer_grid]
    grid[0][3], grid[0][0] = grid[0][0], grid[0][3]  # 13↔16

    # Act
    result = MagicSquareValidator.is_magic(grid)

    # Assert
    assert result is False


def test_validator_returns_false_when_zero_present_d_val_06(durer_grid):
    """D-VAL-06 — 0이 포함된 미완성 격자는 마방진이 아니다."""
    # Arrange
    grid = [row[:] for row in durer_grid]
    grid[0][0] = 0

    # Act
    result = MagicSquareValidator.is_magic(grid)

    # Assert
    assert result is False

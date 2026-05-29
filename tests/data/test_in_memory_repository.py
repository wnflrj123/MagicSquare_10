"""DAT-MEM-* — InMemoryRepository 영속성 계약 테스트.

보호: Repository 인터페이스 계약 (LSP — File 구현체도 동일 테스트 통과해야 함)
FR: FR-09 보조 (PRD §6 FR-09)
"""
import pytest

from boundary.repository.in_memory_repository import InMemoryRepository


def test_save_then_load_returns_same_grid_dat_mem_01():
    """DAT-MEM-01 — save 후 load 시 동일 격자 반환."""
    # Arrange
    repo = InMemoryRepository()
    grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

    # Act
    repo.save_input("g-001", grid)
    loaded = repo.load_input("g-001")

    # Assert
    assert loaded == grid


def test_load_nonexistent_raises_not_found_dat_mem_02():
    """DAT-MEM-02 — 미존재 id 로드 시 NOT_FOUND 예외."""
    # Arrange
    repo = InMemoryRepository()

    # Act / Assert
    with pytest.raises(KeyError):
        repo.load_input("nonexistent")


def test_save_duplicate_id_raises_dat_mem_03():
    """DAT-MEM-03 — 동일 id 두 번 save 시 DUPLICATE_ID 예외."""
    # Arrange
    repo = InMemoryRepository()
    grid = [[0] * 4 for _ in range(4)]

    # Act / Assert
    repo.save_input("g-001", grid)
    with pytest.raises(ValueError):
        repo.save_input("g-001", grid)


def test_saved_grid_preserves_4x4_shape_dat_mem_04():
    """DAT-MEM-04 — 저장된 격자의 shape이 4×4로 유지된다."""
    # Arrange
    repo = InMemoryRepository()
    grid = [[i * 4 + j + 1 for j in range(4)] for i in range(4)]

    # Act
    repo.save_input("g-001", grid)
    loaded = repo.load_input("g-001")

    # Assert
    assert len(loaded) == 4
    assert all(len(row) == 4 for row in loaded)


def test_exists_returns_bool_before_and_after_save_dat_mem_05():
    """DAT-MEM-05 — exists()는 save 전 False, save 후 True."""
    # Arrange
    repo = InMemoryRepository()

    # Act / Assert
    assert repo.exists("g-001") is False
    repo.save_input("g-001", [[0] * 4 for _ in range(4)])
    assert repo.exists("g-001") is True

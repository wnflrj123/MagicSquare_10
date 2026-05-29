"""Warmup smoke tests for User entity.

본 테스트는 MagicSquare Solver 도메인의 일부가 **아니다**. .cursorrules의
ai_behavior·architecture·code_style 규약이 실제 코드 생성에 반영되는지
확인하는 워밍업 (워크북 L895~908). Solver 도메인 진입 시 본 모듈은 제거 가능.

AAA pattern + Google docstring + type hints + entity/ 폴더 배치를 모두 시연.
"""
from entity.user import User


def test_user_creation_stores_id_name_email():
    """User 생성자가 id·name·email 3개 필드를 그대로 저장한다."""
    # Arrange
    user_id = "u-001"
    user_name = "Alice"
    user_email = "alice@example.com"

    # Act
    user = User(id=user_id, name=user_name, email=user_email)

    # Assert
    assert user.id == user_id
    assert user.name == user_name
    assert user.email == user_email

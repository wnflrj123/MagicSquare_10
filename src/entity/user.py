"""User entity — ECB pattern warmup example.

본 모듈은 .cursorrules의 architecture·code_style·ai_behavior 규약이
실제 코드에 반영되는지 검증하는 워밍업이다. MagicSquare Solver 도메인의
일부가 아니며, Solver 코드 진입 시 제거 가능.

본 모듈이 시연하는 .cursorrules 규약:
- architecture.layers.entity 경로 (src/entity/)
- code_style.type_hints (파라미터·반환 모두)
- code_style.docstring (Google 스타일)
- code_style.max_line_length (88, Black 기준)
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Represents a user entity in the system.

    Args:
        id: 사용자 식별자 (Entity identity).
        name: 사용자 표시명.
        email: 사용자 이메일 주소.
    """

    id: str
    name: str
    email: str

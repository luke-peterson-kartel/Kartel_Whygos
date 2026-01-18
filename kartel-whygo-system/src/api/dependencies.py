"""
FastAPI Dependency Injection

Provides repository and service singletons,
plus authentication/authorization dependencies.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional

from ..repositories.json_repository import JsonWhygoRepository, JsonProgressRepository
from ..services.whygo_service import WhygoService
from ..services.progress_service import ProgressService
from ..services.user_service import UserService
from ..services.onboarding_service import OnboardingService
from ..services.validation_service import ValidationService
from ..models.api_models import TokenData
from .config import settings


# HTTP Bearer token security
security = HTTPBearer()

# Repository singletons (load data once, reuse in memory)
_whygo_repo: Optional[JsonWhygoRepository] = None
_progress_repo: Optional[JsonProgressRepository] = None


def get_whygo_repository() -> JsonWhygoRepository:
    """Get or create the WhyGO repository singleton"""
    global _whygo_repo
    if _whygo_repo is None:
        _whygo_repo = JsonWhygoRepository(data_dir=settings.data_dir)
    return _whygo_repo


def get_progress_repository() -> JsonProgressRepository:
    """Get or create the Progress repository singleton"""
    global _progress_repo
    if _progress_repo is None:
        _progress_repo = JsonProgressRepository(data_dir=settings.data_dir)
    return _progress_repo


# Service factories
def get_whygo_service(
    repo: JsonWhygoRepository = Depends(get_whygo_repository)
) -> WhygoService:
    """Create WhygoService with injected repository"""
    return WhygoService(repo)


def get_progress_service(
    whygo_repo: JsonWhygoRepository = Depends(get_whygo_repository),
    progress_repo: JsonProgressRepository = Depends(get_progress_repository)
) -> ProgressService:
    """Create ProgressService with injected repositories"""
    return ProgressService(whygo_repo, progress_repo)


def get_user_service(
    repo: JsonWhygoRepository = Depends(get_whygo_repository)
) -> UserService:
    """Create UserService with injected repository"""
    return UserService(repo)


def get_onboarding_service(
    repo: JsonWhygoRepository = Depends(get_whygo_repository)
) -> OnboardingService:
    """Create OnboardingService with injected repository"""
    return OnboardingService(repo)


def get_validation_service(
    repo: JsonWhygoRepository = Depends(get_whygo_repository)
) -> ValidationService:
    """Create ValidationService with injected repository"""
    return ValidationService(repo)


# Authentication/Authorization
def decode_token(token: str) -> TokenData:
    """
    Decode and validate JWT token

    Args:
        token: JWT token string

    Returns:
        TokenData with person_id, email, level

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        person_id: str = payload.get("sub")
        if person_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject"
            )

        return TokenData(
            person_id=person_id,
            email=payload.get("email"),
            level=payload.get("level"),
            exp=payload.get("exp")
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
) -> dict:
    """
    Get current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer token from Authorization header
        user_service: UserService for fetching user profile

    Returns:
        dict with 'person', 'department', 'manager', 'direct_reports'

    Raises:
        HTTPException: If token invalid or user not found
    """
    token_data = decode_token(credentials.credentials)

    user_profile = user_service.get_user_profile(token_data.person_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user_profile


def require_level(required_level: str):
    """
    Dependency factory for role-based access control

    Usage:
        @router.get("/admin", dependencies=[Depends(require_level("executive"))])

    Args:
        required_level: Minimum level required (ic, manager, department_head, executive)

    Returns:
        Dependency function that checks user level
    """
    def level_checker(current_user: dict = Depends(get_current_user)):
        levels = ['ic', 'manager', 'department_head', 'executive']

        user_level = current_user['person'].level
        if user_level not in levels:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Unknown user level: {user_level}"
            )

        user_level_index = levels.index(user_level)
        required_level_index = levels.index(required_level)

        if user_level_index < required_level_index:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_level} level or higher"
            )

        return current_user

    return level_checker

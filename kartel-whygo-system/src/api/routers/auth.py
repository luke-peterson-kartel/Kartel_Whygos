"""
Authentication Router

Handles login/logout endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from datetime import datetime, timedelta

from ..dependencies import get_user_service, settings
from ...services.user_service import UserService
from ...models.api_models import LoginRequest, Token


router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    """
    Simple email-based login (no password for MVP)

    Looks up user by email and returns JWT token if found.
    """
    # Find person by email
    person = user_service.repo.get_person_by_email(request.email)

    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found in system"
        )

    # Record login timestamp
    user_service.record_login(person.id)

    # Create JWT token
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": person.id,  # Subject = person_id
        "email": person.email,
        "level": person.level,
        "exp": expire
    }

    access_token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        person_id=person.id,
        name=person.name,
        level=person.level
    )


@router.post("/logout")
def logout():
    """
    Logout endpoint

    Client should delete the JWT token on logout.
    Server doesn't need to do anything (stateless JWT).
    """
    return {"message": "Logged out successfully"}

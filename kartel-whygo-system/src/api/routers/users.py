"""
Users Router

Handles user profile and team endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..dependencies import get_current_user, get_user_service
from ...services.user_service import UserService
from ...models.api_models import PersonResponse, PersonProfileUpdate


router = APIRouter()


@router.get("/me", response_model=PersonResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's profile"""
    person = current_user['person']
    return PersonResponse(
        id=person.id,
        name=person.name,
        title=person.title,
        email=person.email,
        department_id=person.department_id,
        manager_id=person.manager_id,
        level=person.level,
        employment_type=person.employment_type,
        status=person.status,
        onboarding_status=person.onboarding_status,
        last_login=person.last_login,
        timezone=person.timezone,
        notification_enabled=person.notification_enabled
    )


@router.put("/me", response_model=PersonResponse)
def update_my_profile(
    updates: PersonProfileUpdate,
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update current user's profile"""
    person_id = current_user['person'].id

    # Only update fields that were provided (exclude None values)
    update_dict = updates.model_dump(exclude_none=True)

    success = user_service.update_profile(person_id, **update_dict)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update failed"
        )

    # Get updated profile
    updated_profile = user_service.get_user_profile(person_id)
    person = updated_profile['person']

    return PersonResponse(
        id=person.id,
        name=person.name,
        title=person.title,
        email=person.email,
        department_id=person.department_id,
        manager_id=person.manager_id,
        level=person.level,
        employment_type=person.employment_type,
        status=person.status,
        onboarding_status=person.onboarding_status,
        last_login=person.last_login,
        timezone=person.timezone,
        notification_enabled=person.notification_enabled
    )


@router.get("/me/team", response_model=List[PersonResponse])
def get_my_team(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user's team members (same department)"""
    person_id = current_user['person'].id
    team_members = user_service.get_team_members(person_id)

    return [
        PersonResponse(
            id=p.id,
            name=p.name,
            title=p.title,
            email=p.email,
            department_id=p.department_id,
            manager_id=p.manager_id,
            level=p.level,
            employment_type=p.employment_type,
            status=p.status,
            onboarding_status=p.onboarding_status,
            last_login=p.last_login,
            timezone=p.timezone,
            notification_enabled=p.notification_enabled
        )
        for p in team_members
    ]

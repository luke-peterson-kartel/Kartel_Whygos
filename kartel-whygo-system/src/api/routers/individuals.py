"""
Individual Goals Router - Basic implementation
"""

from fastapi import APIRouter, Depends
from ..dependencies import get_current_user, get_whygo_service

router = APIRouter()

@router.get("/me")
def get_my_goals(
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get current user's individual goals"""
    person_id = current_user['person'].id
    goals = whygo_service.repo.get_individual_goals_by_person(person_id)
    return [{"id": g.id, "goal": g.goal, "status": g.status} for g in goals]

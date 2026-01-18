"""
Outcomes & Progress Router - Basic implementation
"""

from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user, get_whygo_service, get_progress_service

router = APIRouter()

@router.get("/{outcome_id}")
def get_outcome_details(
    outcome_id: str,
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get detailed outcome information"""
    outcome = whygo_service.repo.get_outcome(outcome_id)
    if not outcome:
        raise HTTPException(status_code=404, detail="Outcome not found")

    return {
        "id": outcome.id,
        "description": outcome.description,
        "metric_type": outcome.metric_type,
        "owner_id": outcome.owner_id,
        "target_q1": outcome.target_q1,
        "target_q2": outcome.target_q2,
        "target_q3": outcome.target_q3,
        "target_q4": outcome.target_q4,
        "actual_q1": outcome.actual_q1,
        "actual_q2": outcome.actual_q2,
        "actual_q3": outcome.actual_q3,
        "actual_q4": outcome.actual_q4,
        "status_q1": outcome.status_q1,
        "status_q2": outcome.status_q2,
        "status_q3": outcome.status_q3,
        "status_q4": outcome.status_q4,
    }

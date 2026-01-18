"""
Company Goals Router - Basic implementation
"""

from fastapi import APIRouter, Depends
from ..dependencies import get_current_user, get_whygo_service

router = APIRouter()

@router.get("/goals")
def get_company_goals(
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get all company goals"""
    goals = whygo_service.repo.get_all_company_goals()
    return [
        {
            "id": g.id,
            "why": g.why,
            "goal": g.goal,
            "status": g.status,
            "owner_id": g.owner_id,
            "fiscal_year": g.fiscal_year,
            "outcomes": [
                {
                    "id": o.id,
                    "description": o.description,
                    "metric_type": o.metric_type,
                    "owner_id": o.owner_id,
                    "target_q1": o.target_q1,
                    "target_q2": o.target_q2,
                    "target_q3": o.target_q3,
                    "target_q4": o.target_q4,
                }
                for o in g.outcomes
            ]
        }
        for g in goals
    ]


@router.get("/dashboard")
def get_company_dashboard(
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get company dashboard with summary stats"""
    return whygo_service.get_company_dashboard_data()

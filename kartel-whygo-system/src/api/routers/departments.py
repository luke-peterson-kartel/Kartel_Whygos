"""
Departments Router - Basic implementation
"""

from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user, get_whygo_service

router = APIRouter()

@router.get("/me/goals")
def get_my_department_goals(
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get goals for current user's department"""
    dept_id = current_user['person'].department_id
    if not dept_id:
        return []

    goals = whygo_service.repo.get_department_goals_by_department(dept_id)
    return [
        {
            "id": g.id,
            "department_id": g.department_id,
            "parent_goal_ids": g.parent_goal_ids,
            "why": g.why,
            "goal": g.goal,
            "status": g.status,
            "fiscal_year": g.fiscal_year,
            "outcomes": [
                {
                    "id": o.id,
                    "description": o.description,
                    "metric_type": o.metric_type,
                    "owner_id": o.owner_id,
                    "target_annual": o.target_annual,
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


@router.get("/{dept_id}/goals")
def get_department_goals(
    dept_id: str,
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get all goals for a department"""
    goals = whygo_service.repo.get_department_goals_by_department(dept_id)
    return [
        {
            "id": g.id,
            "department_id": g.department_id,
            "parent_goal_ids": g.parent_goal_ids,
            "why": g.why,
            "goal": g.goal,
            "status": g.status,
            "fiscal_year": g.fiscal_year,
            "outcomes": [
                {
                    "id": o.id,
                    "description": o.description,
                    "metric_type": o.metric_type,
                    "owner_id": o.owner_id,
                    "target_annual": o.target_annual,
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


@router.get("/{dept_id}/dashboard")
def get_department_dashboard(
    dept_id: str,
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get department dashboard"""
    dashboard = whygo_service.get_department_dashboard_data(dept_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Department not found")
    return dashboard

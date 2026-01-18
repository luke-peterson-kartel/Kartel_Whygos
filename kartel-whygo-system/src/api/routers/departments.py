"""
Departments Router - Basic implementation
"""

from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_current_user, get_whygo_service

router = APIRouter()

@router.get("/{dept_id}/goals")
def get_department_goals(
    dept_id: str,
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get all goals for a department"""
    goals = whygo_service.repo.get_department_goals_by_department(dept_id)
    return [{"id": g.id, "goal": g.goal, "status": g.status} for g in goals]


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

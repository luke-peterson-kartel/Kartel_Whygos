"""
Onboarding Router

Handles onboarding flow endpoints
"""

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_current_user, get_onboarding_service
from ...services.onboarding_service import OnboardingService
from ...models.api_models import OnboardingContext


router = APIRouter()


@router.get("/context", response_model=OnboardingContext)
def get_onboarding_context(
    current_user: dict = Depends(get_current_user),
    onboarding_service: OnboardingService = Depends(get_onboarding_service)
):
    """
    Get all context needed for onboarding interface:
    - User profile
    - Company goals
    - Department goals
    - Existing individual goals
    - Pending approvals (if manager)
    """
    person_id = current_user['person'].id
    context = onboarding_service.get_onboarding_context(person_id)

    if not context:
        raise HTTPException(status_code=404, detail="Context not found")

    # Convert dataclasses to Pydantic models
    from ...models.api_models import (
        PersonResponse, DepartmentResponse,
        CompanyGoalResponse, DepartmentGoalResponse,
        IndividualGoalResponse, OutcomeResponse
    )

    def person_to_response(p):
        if not p:
            return None
        return PersonResponse(
            id=p.id, name=p.name, title=p.title, email=p.email,
            department_id=p.department_id, manager_id=p.manager_id,
            level=p.level, employment_type=p.employment_type,
            status=p.status, onboarding_status=p.onboarding_status,
            last_login=p.last_login, timezone=p.timezone,
            notification_enabled=p.notification_enabled
        )

    def dept_to_response(d):
        if not d:
            return None
        return DepartmentResponse(
            id=d.id, name=d.name, head_id=d.head_id,
            primary_company_goal_ids=d.primary_company_goal_ids,
            secondary_company_goal_ids=d.secondary_company_goal_ids,
            reports_to=d.reports_to
        )

    def outcome_to_response(o):
        return OutcomeResponse(
            id=o.id, goal_id=o.goal_id, description=o.description,
            metric_type=o.metric_type, owner_id=o.owner_id,
            target_annual=o.target_annual, target_q1=o.target_q1,
            target_q2=o.target_q2, target_q3=o.target_q3, target_q4=o.target_q4,
            actual_q1=o.actual_q1, actual_q2=o.actual_q2,
            actual_q3=o.actual_q3, actual_q4=o.actual_q4,
            status_q1=o.status_q1, status_q2=o.status_q2,
            status_q3=o.status_q3, status_q4=o.status_q4
        )

    def company_goal_to_response(g):
        return CompanyGoalResponse(
            id=g.id, why=g.why, goal=g.goal, status=g.status,
            owner_id=g.owner_id, fiscal_year=g.fiscal_year,
            outcomes=[outcome_to_response(o) for o in g.outcomes],
            created_at=g.created_at, updated_at=g.updated_at
        )

    def dept_goal_to_response(g):
        return DepartmentGoalResponse(
            id=g.id, department_id=g.department_id,
            parent_goal_ids=g.parent_goal_ids, why=g.why, goal=g.goal,
            status=g.status, approved_by=g.approved_by,
            fiscal_year=g.fiscal_year,
            outcomes=[outcome_to_response(o) for o in g.outcomes],
            created_at=g.created_at, updated_at=g.updated_at
        )

    def indiv_goal_to_response(g):
        return IndividualGoalResponse(
            id=g.id, person_id=g.person_id,
            parent_goal_ids=g.parent_goal_ids, why=g.why, goal=g.goal,
            status=g.status, approved_by=g.approved_by,
            fiscal_year=g.fiscal_year,
            outcomes=[outcome_to_response(o) for o in g.outcomes],
            created_at=g.created_at, updated_at=g.updated_at
        )

    return OnboardingContext(
        person=person_to_response(context['person']),
        department=dept_to_response(context['department']),
        manager=person_to_response(context['manager']),
        company_goals=[company_goal_to_response(g) for g in context['company_goals']],
        department_goals=[dept_goal_to_response(g) for g in context['department_goals']],
        individual_goals=[indiv_goal_to_response(g) for g in context['individual_goals']],
        pending_approvals=[indiv_goal_to_response(g) for g in context['pending_approvals']]
    )


@router.post("/start")
def start_onboarding(
    current_user: dict = Depends(get_current_user),
    onboarding_service: OnboardingService = Depends(get_onboarding_service)
):
    """Mark onboarding as started"""
    person_id = current_user['person'].id
    success = onboarding_service.start_onboarding(person_id)

    if not success:
        raise HTTPException(status_code=400, detail="Cannot start onboarding")

    return {"message": "Onboarding started", "person_id": person_id}


@router.post("/complete")
def complete_onboarding(
    current_user: dict = Depends(get_current_user),
    onboarding_service: OnboardingService = Depends(get_onboarding_service)
):
    """Mark onboarding as completed"""
    person_id = current_user['person'].id
    success = onboarding_service.complete_onboarding(person_id)

    if not success:
        raise HTTPException(status_code=400, detail="Cannot complete onboarding")

    return {"message": "Onboarding completed", "person_id": person_id}

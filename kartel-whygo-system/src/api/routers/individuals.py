"""
Individual Goals Router - Basic implementation
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..dependencies import get_current_user, get_whygo_service
from ...models.whygo import IndividualWhyGO, Outcome

router = APIRouter()


class OutcomeCreate(BaseModel):
    description: str
    metric_type: str
    owner_id: str
    target_annual: float
    target_q1: Optional[float] = None
    target_q2: Optional[float] = None
    target_q3: Optional[float] = None
    target_q4: Optional[float] = None


class CreateGoalRequest(BaseModel):
    parent_goal_ids: List[str]
    why: str
    goal: str
    outcomes: List[OutcomeCreate]


@router.get("/me")
def get_my_goals(
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Get current user's individual goals"""
    person_id = current_user['person'].id
    goals = whygo_service.repo.get_individual_goals_by_person(person_id)

    # Return full goal details with outcomes (outcomes are already embedded in goal object)
    result = []
    for g in goals:
        result.append({
            "id": g.id,
            "person_id": g.person_id,
            "parent_goal_ids": g.parent_goal_ids,
            "why": g.why,
            "goal": g.goal,
            "status": g.status,
            "approved_by": g.approved_by,
            "fiscal_year": g.fiscal_year,
            "outcomes": [
                {
                    "id": o.id,
                    "goal_id": o.goal_id,
                    "description": o.description,
                    "metric_type": o.metric_type,
                    "owner_id": o.owner_id,
                    "target_annual": o.target_annual,
                    "target_q1": o.target_q1,
                    "target_q2": o.target_q2,
                    "target_q3": o.target_q3,
                    "target_q4": o.target_q4,
                    "actual_q1": o.actual_q1,
                    "actual_q2": o.actual_q2,
                    "actual_q3": o.actual_q3,
                    "actual_q4": o.actual_q4,
                    "status_q1": o.status_q1,
                    "status_q2": o.status_q2,
                    "status_q3": o.status_q3,
                    "status_q4": o.status_q4
                }
                for o in g.outcomes
            ],
            "created_at": g.created_at,
            "updated_at": g.updated_at
        })
    return result


@router.post("/create", status_code=201)
def create_my_goal(
    request: CreateGoalRequest,
    current_user: dict = Depends(get_current_user),
    whygo_service = Depends(get_whygo_service)
):
    """Create a new individual goal for the current user"""
    person_id = current_user['person'].id

    # Validate: Check max 3 goals
    existing_goals = whygo_service.repo.get_individual_goals_by_person(person_id)
    if len(existing_goals) >= 3:
        raise HTTPException(status_code=400, detail="Maximum 3 goals allowed per person")

    # Validate: 2-3 outcomes required
    if len(request.outcomes) < 2 or len(request.outcomes) > 3:
        raise HTTPException(status_code=400, detail="Must provide 2-3 outcomes per goal")

    # Generate IDs
    goal_id = f"ig_{person_id.replace('person_', '')}_{len(existing_goals) + 1}"

    # Create outcomes first
    outcomes = []
    for idx, o in enumerate(request.outcomes):
        outcome_id = f"{goal_id}_o{idx + 1}"
        outcome = Outcome(
            id=outcome_id,
            goal_id=goal_id,
            description=o.description,
            metric_type=o.metric_type,
            owner_id=o.owner_id,
            target_annual=o.target_annual,
            target_q1=o.target_q1,
            target_q2=o.target_q2,
            target_q3=o.target_q3,
            target_q4=o.target_q4,
            actual_q1=None,
            actual_q2=None,
            actual_q3=None,
            actual_q4=None,
            status_q1=None,
            status_q2=None,
            status_q3=None,
            status_q4=None
        )
        outcomes.append(outcome)

    # Create goal object with outcomes
    goal = IndividualWhyGO(
        id=goal_id,
        person_id=person_id,
        parent_goal_ids=request.parent_goal_ids,
        why=request.why,
        goal=request.goal,
        status="pending_approval",
        approved_by=None,
        fiscal_year=2026,
        outcomes=outcomes,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

    # Create goal in repository
    success = whygo_service.repo.create_individual_goal(goal)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create goal")

    # Save to disk
    whygo_service.repo.save_all()

    # Return the created goal
    return {
        "id": goal.id,
        "person_id": goal.person_id,
        "parent_goal_ids": goal.parent_goal_ids,
        "why": goal.why,
        "goal": goal.goal,
        "status": goal.status,
        "approved_by": goal.approved_by,
        "fiscal_year": goal.fiscal_year,
        "outcomes": [
            {
                "id": o.id,
                "goal_id": o.goal_id,
                "description": o.description,
                "metric_type": o.metric_type,
                "owner_id": o.owner_id,
                "target_annual": o.target_annual,
                "target_q1": o.target_q1,
                "target_q2": o.target_q2,
                "target_q3": o.target_q3,
                "target_q4": o.target_q4,
                "actual_q1": o.actual_q1,
                "actual_q2": o.actual_q2,
                "actual_q3": o.actual_q3,
                "actual_q4": o.actual_q4,
                "status_q1": o.status_q1,
                "status_q2": o.status_q2,
                "status_q3": o.status_q3,
                "status_q4": o.status_q4
            }
            for o in goal.outcomes
        ],
        "created_at": goal.created_at,
        "updated_at": goal.updated_at
    }

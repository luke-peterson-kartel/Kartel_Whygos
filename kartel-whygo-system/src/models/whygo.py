"""
WhyGO Data Models

Python dataclasses matching the TypeScript schemas from DATA_STRUCTURES.md
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal, Union
from datetime import datetime


@dataclass
class Outcome:
    """Outcome with quarterly targets and actuals"""
    id: str
    goal_id: str
    description: str
    metric_type: Literal['number', 'percentage', 'currency', 'boolean', 'milestone']
    owner_id: str

    # Targets (set at goal creation)
    target_annual: Union[int, float, str]
    target_q1: Union[int, float, str, None]
    target_q2: Union[int, float, str, None]
    target_q3: Union[int, float, str, None]
    target_q4: Union[int, float, str, None]

    # Actuals (updated during tracking)
    actual_q1: Union[int, float, str, None] = None
    actual_q2: Union[int, float, str, None] = None
    actual_q3: Union[int, float, str, None] = None
    actual_q4: Union[int, float, str, None] = None

    # Calculated status
    status_q1: Optional[Literal['+', '~', '-']] = None
    status_q2: Optional[Literal['+', '~', '-']] = None
    status_q3: Optional[Literal['+', '~', '-']] = None
    status_q4: Optional[Literal['+', '~', '-']] = None


@dataclass
class ProgressUpdate:
    """Progress update record for tracking changes to outcomes"""
    id: str
    outcome_id: str
    quarter: Literal['Q1', 'Q2', 'Q3', 'Q4']
    actual_value: Union[int, float, str, None]
    status: Optional[Literal['+', '~', '-']]
    notes: Optional[str] = None
    blocker: Optional[str] = None
    recorded_by: str = ""  # Person.id
    recorded_at: str = ""  # ISO timestamp


@dataclass
class CompanyWhyGO:
    """Company-level WhyGO"""
    id: str
    level: Literal['company'] = 'company'
    why: str = ""
    goal: str = ""
    status: Literal['draft', 'pending_approval', 'approved', 'archived'] = 'draft'
    owner_id: str = ""
    fiscal_year: int = 2026
    outcomes: List[Outcome] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class DepartmentWhyGO:
    """Department-level WhyGO"""
    id: str
    level: Literal['department'] = 'department'
    department_id: str = ""
    parent_goal_ids: List[str] = field(default_factory=list)
    why: str = ""
    goal: str = ""
    status: Literal['draft', 'pending_approval', 'approved', 'archived'] = 'draft'
    approved_by: Optional[str] = None
    fiscal_year: int = 2026
    outcomes: List[Outcome] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class IndividualWhyGO:
    """Individual-level WhyGO"""
    id: str
    level: Literal['individual'] = 'individual'
    person_id: str = ""
    parent_goal_ids: List[str] = field(default_factory=list)
    why: str = ""
    goal: str = ""
    status: Literal['draft', 'pending_approval', 'approved', 'archived'] = 'draft'
    approved_by: Optional[str] = None
    fiscal_year: int = 2026
    outcomes: List[Outcome] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Person:
    """Employee/Person"""
    id: str
    name: str
    title: str
    department_id: str
    manager_id: Optional[str]
    level: Literal['executive', 'department_head', 'manager', 'ic']
    employment_type: Literal['w2', 'contractor', 'international', 'trial'] = 'w2'
    status: Literal['active', 'trial', 'searching'] = 'active'


@dataclass
class Department:
    """Department"""
    id: str
    name: str
    head_id: str
    primary_company_goal_ids: List[str]
    secondary_company_goal_ids: List[str]
    reports_to: Optional[str] = None


def whygo_to_dict(whygo: Union[CompanyWhyGO, DepartmentWhyGO, IndividualWhyGO]) -> dict:
    """Convert a WhyGO object to a dictionary for JSON serialization"""
    result = {
        "id": whygo.id,
        "level": whygo.level,
        "why": whygo.why,
        "goal": whygo.goal,
        "status": whygo.status,
        "fiscal_year": whygo.fiscal_year,
        "outcomes": [outcome_to_dict(o) for o in whygo.outcomes]
    }

    if isinstance(whygo, CompanyWhyGO):
        result["owner_id"] = whygo.owner_id
    elif isinstance(whygo, DepartmentWhyGO):
        result["department_id"] = whygo.department_id
        result["parent_goal_ids"] = whygo.parent_goal_ids
        result["approved_by"] = whygo.approved_by
    elif isinstance(whygo, IndividualWhyGO):
        result["person_id"] = whygo.person_id
        result["parent_goal_ids"] = whygo.parent_goal_ids
        result["approved_by"] = whygo.approved_by

    if whygo.created_at:
        result["created_at"] = whygo.created_at
    if whygo.updated_at:
        result["updated_at"] = whygo.updated_at

    return result


def outcome_to_dict(outcome: Outcome) -> dict:
    """Convert an Outcome object to a dictionary for JSON serialization"""
    return {
        "id": outcome.id,
        "goal_id": outcome.goal_id,
        "description": outcome.description,
        "metric_type": outcome.metric_type,
        "owner_id": outcome.owner_id,
        "target_annual": outcome.target_annual,
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
        "status_q4": outcome.status_q4
    }


def person_to_dict(person: Person) -> dict:
    """Convert a Person object to a dictionary"""
    return {
        "id": person.id,
        "name": person.name,
        "title": person.title,
        "department_id": person.department_id,
        "manager_id": person.manager_id,
        "level": person.level,
        "employment_type": person.employment_type,
        "status": person.status
    }


def department_to_dict(dept: Department) -> dict:
    """Convert a Department object to a dictionary"""
    return {
        "id": dept.id,
        "name": dept.name,
        "head_id": dept.head_id,
        "primary_company_goal_ids": dept.primary_company_goal_ids,
        "secondary_company_goal_ids": dept.secondary_company_goal_ids,
        "reports_to": dept.reports_to
    }


def progress_update_to_dict(update: ProgressUpdate) -> dict:
    """Convert a ProgressUpdate object to a dictionary"""
    return {
        "id": update.id,
        "outcome_id": update.outcome_id,
        "quarter": update.quarter,
        "actual_value": update.actual_value,
        "status": update.status,
        "notes": update.notes,
        "blocker": update.blocker,
        "recorded_by": update.recorded_by,
        "recorded_at": update.recorded_at
    }

"""
Pydantic models for FastAPI request/response validation
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime


# Authentication Models
class TokenData(BaseModel):
    person_id: str
    email: Optional[str] = None
    level: str
    exp: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    person_id: str
    name: str
    level: str


class LoginRequest(BaseModel):
    email: EmailStr


# User/Person Models
class PersonResponse(BaseModel):
    id: str
    name: str
    title: str
    email: Optional[str]
    department_id: str
    manager_id: Optional[str]
    level: str
    employment_type: str
    status: str
    onboarding_status: str
    last_login: Optional[str]
    timezone: str
    notification_enabled: bool

    class Config:
        from_attributes = True


class PersonProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    timezone: Optional[str] = None
    notification_enabled: Optional[bool] = None


# Outcome Models
class OutcomeResponse(BaseModel):
    id: str
    goal_id: str
    description: str
    metric_type: str
    owner_id: str
    target_annual: Optional[float] = None
    target_q1: Optional[float] = None
    target_q2: Optional[float] = None
    target_q3: Optional[float] = None
    target_q4: Optional[float] = None
    actual_q1: Optional[float] = None
    actual_q2: Optional[float] = None
    actual_q3: Optional[float] = None
    actual_q4: Optional[float] = None
    status_q1: Optional[str] = None
    status_q2: Optional[str] = None
    status_q3: Optional[str] = None
    status_q4: Optional[str] = None

    class Config:
        from_attributes = True


class CreateOutcome(BaseModel):
    description: str = Field(..., min_length=1)
    metric_type: Literal['number', 'percentage', 'currency', 'boolean', 'milestone']
    owner_id: str
    target_annual: float
    target_q1: Optional[float] = None
    target_q2: Optional[float] = None
    target_q3: Optional[float] = None
    target_q4: Optional[float] = None


# Goal Response Models
class CompanyGoalResponse(BaseModel):
    id: str
    why: str
    goal: str
    status: str
    owner_id: str
    fiscal_year: int
    outcomes: List[OutcomeResponse]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class DepartmentGoalResponse(BaseModel):
    id: str
    department_id: str
    parent_goal_ids: List[str]
    why: str
    goal: str
    status: str
    approved_by: Optional[str]
    fiscal_year: int
    outcomes: List[OutcomeResponse]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class IndividualGoalResponse(BaseModel):
    id: str
    person_id: str
    parent_goal_ids: List[str]
    why: str
    goal: str
    status: str
    approved_by: Optional[str]
    fiscal_year: int
    outcomes: List[OutcomeResponse]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# Goal Creation Models
class CreateIndividualGoal(BaseModel):
    parent_goal_ids: List[str] = Field(..., min_length=1)
    why: str = Field(..., max_length=500)
    goal: str = Field(..., max_length=300)
    outcomes: List[CreateOutcome] = Field(..., min_length=2, max_length=3)


# Progress Tracking Models
class RecordProgress(BaseModel):
    quarter: Literal['Q1', 'Q2', 'Q3', 'Q4']
    actual_value: float
    notes: Optional[str] = None
    blocker: Optional[str] = None


# Department Model
class DepartmentResponse(BaseModel):
    id: str
    name: str
    head_id: str
    primary_company_goal_ids: List[str]
    secondary_company_goal_ids: List[str]
    reports_to: Optional[str] = None

    class Config:
        from_attributes = True


# Onboarding Context Model
class OnboardingContext(BaseModel):
    person: PersonResponse
    department: Optional[DepartmentResponse]
    manager: Optional[PersonResponse]
    company_goals: List[CompanyGoalResponse]
    department_goals: List[DepartmentGoalResponse]
    individual_goals: List[IndividualGoalResponse]
    pending_approvals: List[IndividualGoalResponse]

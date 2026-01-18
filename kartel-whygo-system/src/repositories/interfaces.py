"""
Abstract repository interfaces for data access layer

These interfaces define the contract for data operations.
Implementations can use JSON files, databases, or any other storage backend.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.whygo import (
    CompanyWhyGO,
    DepartmentWhyGO,
    IndividualWhyGO,
    Outcome,
    ProgressUpdate
)


class IWhygoRepository(ABC):
    """Abstract interface for WhyGO data operations"""

    @abstractmethod
    def get_all_company_goals(self) -> List[CompanyWhyGO]:
        """Get all company-level WhyGOs"""
        pass

    @abstractmethod
    def get_company_goal(self, goal_id: str) -> Optional[CompanyWhyGO]:
        """Get a specific company WhyGO by ID"""
        pass

    @abstractmethod
    def get_all_department_goals(self) -> List[DepartmentWhyGO]:
        """Get all department-level WhyGOs"""
        pass

    @abstractmethod
    def get_department_goals_by_department(self, dept_id: str) -> List[DepartmentWhyGO]:
        """Get all WhyGOs for a specific department"""
        pass

    @abstractmethod
    def get_all_individual_goals(self) -> List[IndividualWhyGO]:
        """Get all individual-level WhyGOs"""
        pass

    @abstractmethod
    def get_individual_goals_by_person(self, person_id: str) -> List[IndividualWhyGO]:
        """Get all WhyGOs for a specific person"""
        pass

    @abstractmethod
    def get_outcome(self, outcome_id: str) -> Optional[Outcome]:
        """Find an outcome by ID across all goals"""
        pass

    @abstractmethod
    def update_outcome(self, outcome: Outcome) -> bool:
        """Update an outcome (typically after recording progress)"""
        pass

    @abstractmethod
    def save_all(self) -> bool:
        """Persist all changes to storage backend"""
        pass


class IProgressRepository(ABC):
    """Abstract interface for progress update operations"""

    @abstractmethod
    def record_progress(self, update: ProgressUpdate) -> bool:
        """Record a progress update"""
        pass

    @abstractmethod
    def get_updates_for_outcome(self, outcome_id: str) -> List[ProgressUpdate]:
        """Get all progress updates for a specific outcome"""
        pass

    @abstractmethod
    def get_all_updates(self) -> List[ProgressUpdate]:
        """Get all progress updates"""
        pass

    @abstractmethod
    def save_all(self) -> bool:
        """Persist all progress updates to storage"""
        pass

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
    ProgressUpdate,
    Person,
    Department
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

    # Person/User methods
    @abstractmethod
    def get_person(self, person_id: str) -> Optional[Person]:
        """Get a person by ID"""
        pass

    @abstractmethod
    def get_person_by_email(self, email: str) -> Optional[Person]:
        """Get a person by email address"""
        pass

    @abstractmethod
    def get_all_people(self) -> List[Person]:
        """Get all people/employees"""
        pass

    @abstractmethod
    def get_people_by_department(self, dept_id: str) -> List[Person]:
        """Get all people in a specific department"""
        pass

    @abstractmethod
    def update_person(self, person: Person) -> bool:
        """Update a person's information"""
        pass

    # Department methods
    @abstractmethod
    def get_department(self, dept_id: str) -> Optional[Department]:
        """Get a department by ID"""
        pass

    @abstractmethod
    def get_all_departments(self) -> List[Department]:
        """Get all departments"""
        pass

    # Goal creation/update methods
    @abstractmethod
    def create_individual_goal(self, goal: IndividualWhyGO) -> bool:
        """Create a new individual goal"""
        pass

    @abstractmethod
    def update_individual_goal(self, goal: IndividualWhyGO) -> bool:
        """Update an existing individual goal"""
        pass

    @abstractmethod
    def get_goals_by_status(self, status: str) -> dict:
        """Get goals filtered by status (returns dict with company, department, individual)"""
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

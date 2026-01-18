"""
Onboarding Service - Business logic for user onboarding flow
"""

from typing import Optional
from datetime import datetime
from ..models.whygo import Person
from ..repositories.interfaces import IWhygoRepository


class OnboardingService:
    """Service for onboarding flow and context"""

    def __init__(self, repo: IWhygoRepository):
        self.repo = repo

    def get_onboarding_context(self, person_id: str) -> Optional[dict]:
        """
        Get all context needed for onboarding interface

        Returns context including:
        - User's profile
        - Their department
        - Their manager
        - Company goals (all users see these)
        - Department goals (filtered by user's department)
        - Individual goals (user's own goals)
        - Pending approvals (if user is a manager/dept head)

        Args:
            person_id: Person to get context for

        Returns:
            dict with all onboarding context, or None if person not found
        """
        person = self.repo.get_person(person_id)
        if not person:
            return None

        # Get person's department and manager
        department = self.repo.get_department(person.department_id)
        manager = self.repo.get_person(person.manager_id) if person.manager_id else None

        # Get goals - all users see company goals
        company_goals = self.repo.get_all_company_goals()

        # Get department goals for user's department
        dept_goals = self.repo.get_department_goals_by_department(person.department_id)

        # Get user's individual goals
        individual_goals = self.repo.get_individual_goals_by_person(person_id)

        # Get pending approvals if user is a manager/dept head/executive
        pending_approvals = []
        if person.level in ['department_head', 'manager', 'executive']:
            all_pending = self.repo.get_goals_by_status('pending_approval')

            if person.level == 'executive':
                # Executives see all pending individual goals
                pending_approvals = all_pending['individual']
            else:
                # Managers/dept heads see their direct reports' pending goals
                pending_approvals = [
                    g for g in all_pending['individual']
                    if self.repo.get_person(g.person_id).manager_id == person_id
                ]

        return {
            'person': person,
            'department': department,
            'manager': manager,
            'company_goals': company_goals,
            'department_goals': dept_goals,
            'individual_goals': individual_goals,
            'pending_approvals': pending_approvals
        }

    def start_onboarding(self, person_id: str) -> bool:
        """
        Mark onboarding as started for a person

        Args:
            person_id: Person starting onboarding

        Returns:
            bool indicating success
        """
        person = self.repo.get_person(person_id)
        if not person:
            return False

        # Only start if not already started or completed
        if person.onboarding_status != 'not_started':
            return False

        person.onboarding_status = 'in_progress'
        person.onboarding_started_at = datetime.now().isoformat()

        success = self.repo.update_person(person)
        if success:
            self.repo.save_all()

        return success

    def complete_onboarding(self, person_id: str) -> bool:
        """
        Mark onboarding as completed for a person

        Args:
            person_id: Person completing onboarding

        Returns:
            bool indicating success
        """
        person = self.repo.get_person(person_id)
        if not person:
            return False

        # Don't re-complete if already completed
        if person.onboarding_status == 'completed':
            return False

        person.onboarding_status = 'completed'
        person.onboarding_completed_at = datetime.now().isoformat()

        success = self.repo.update_person(person)
        if success:
            self.repo.save_all()

        return success

    def get_onboarding_status(self, person_id: str) -> Optional[dict]:
        """
        Get onboarding status for a person

        Args:
            person_id: Person to check

        Returns:
            dict with status, started_at, completed_at
        """
        person = self.repo.get_person(person_id)
        if not person:
            return None

        return {
            'status': person.onboarding_status,
            'started_at': person.onboarding_started_at,
            'completed_at': person.onboarding_completed_at
        }

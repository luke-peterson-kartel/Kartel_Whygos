"""
User Service - Business logic for user/employee operations
"""

from typing import Optional, List
from datetime import datetime
from ..models.whygo import Person, Department
from ..repositories.interfaces import IWhygoRepository


class UserService:
    """Service for user profile and team operations"""

    def __init__(self, repo: IWhygoRepository):
        self.repo = repo

    def get_user_profile(self, person_id: str) -> Optional[dict]:
        """
        Get complete user profile with related data

        Returns:
            dict with person, department, manager, direct_reports
        """
        person = self.repo.get_person(person_id)
        if not person:
            return None

        department = self.repo.get_department(person.department_id)
        manager = self.repo.get_person(person.manager_id) if person.manager_id else None

        # Get direct reports (people who report to this person)
        all_people = self.repo.get_all_people()
        direct_reports = [p for p in all_people if p.manager_id == person_id]

        return {
            'person': person,
            'department': department,
            'manager': manager,
            'direct_reports': direct_reports
        }

    def update_profile(self, person_id: str, **updates) -> bool:
        """
        Update a person's profile fields

        Args:
            person_id: Person to update
            **updates: Fields to update (email, timezone, notification_enabled, etc.)

        Returns:
            bool indicating success
        """
        person = self.repo.get_person(person_id)
        if not person:
            return False

        # Update only provided fields
        for key, value in updates.items():
            if hasattr(person, key):
                setattr(person, key, value)

        success = self.repo.update_person(person)
        if success:
            self.repo.save_all()

        return success

    def record_login(self, person_id: str) -> bool:
        """
        Record that a user logged in (updates last_login timestamp)

        Args:
            person_id: Person who logged in

        Returns:
            bool indicating success
        """
        return self.update_profile(
            person_id,
            last_login=datetime.now().isoformat()
        )

    def get_team_members(self, person_id: str) -> List[Person]:
        """
        Get all team members (people in the same department)

        Args:
            person_id: Person whose team to fetch

        Returns:
            List of Person objects in the same department
        """
        person = self.repo.get_person(person_id)
        if not person:
            return []

        return self.repo.get_people_by_department(person.department_id)

    def get_direct_reports(self, person_id: str) -> List[Person]:
        """
        Get all people who directly report to this person

        Args:
            person_id: Manager's ID

        Returns:
            List of Person objects who report to this manager
        """
        all_people = self.repo.get_all_people()
        return [p for p in all_people if p.manager_id == person_id]

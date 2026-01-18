"""
Validation Service - Business logic for validating WhyGO rules
"""

from typing import List, Tuple
from ..models.whygo import IndividualWhyGO, Person
from ..repositories.interfaces import IWhygoRepository


class ValidationService:
    """Service for validating WhyGO rules and constraints"""

    def __init__(self, repo: IWhygoRepository):
        self.repo = repo

    def validate_individual_goal(self, goal: IndividualWhyGO) -> Tuple[bool, List[str]]:
        """
        Validate an individual goal against all WhyGO rules

        Rules enforced:
        1. Maximum 3 active goals per person
        2. Must ladder up to at least one department goal (no orphans)
        3. Must have 2-3 outcomes
        4. Each outcome must have an owner and targets

        Args:
            goal: IndividualWhyGO to validate

        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        errors = []

        # Rule 1: Check 3-goal limit
        existing_goals = self.repo.get_individual_goals_by_person(goal.person_id)
        active_goals = [g for g in existing_goals if g.status != 'archived']

        # Don't count the goal itself if it already exists (for updates)
        active_goal_ids = [g.id for g in active_goals]
        if goal.id in active_goal_ids:
            # This is an update to an existing goal, don't count it
            active_count = len(active_goals) - 1
        else:
            # This is a new goal
            active_count = len(active_goals)

        if active_count >= 3:
            errors.append("Maximum 3 goals per person. Archive existing goals first.")

        # Rule 2: Must ladder up to parent goal
        if not goal.parent_goal_ids:
            errors.append("Goal must connect to at least one department goal (no orphan goals).")
        else:
            # Verify parent goals exist and are in the person's department
            person = self.repo.get_person(goal.person_id)
            if person:
                dept_goals = self.repo.get_department_goals_by_department(person.department_id)
                valid_parent_ids = [g.id for g in dept_goals]

                invalid_parents = [pid for pid in goal.parent_goal_ids if pid not in valid_parent_ids]
                if invalid_parents:
                    errors.append(f"Invalid parent goal IDs: {invalid_parents}. Parent goals must be from your department.")
            else:
                errors.append("Person not found.")

        # Rule 3: Must have 2-3 outcomes
        outcome_count = len(goal.outcomes)
        if outcome_count < 2:
            errors.append("Goal must have at least 2 measurable outcomes.")
        if outcome_count > 3:
            errors.append("Goal should have no more than 3 outcomes.")

        # Rule 4: Validate each outcome
        for idx, outcome in enumerate(goal.outcomes, 1):
            outcome_prefix = f"Outcome {idx}"

            if not outcome.owner_id:
                errors.append(f"{outcome_prefix} ('{outcome.description}') must have an owner.")

            if not outcome.description or len(outcome.description.strip()) == 0:
                errors.append(f"{outcome_prefix} must have a description.")

            if outcome.target_annual is None:
                errors.append(f"{outcome_prefix} ('{outcome.description}') must have an annual target.")

            # Check that at least one quarterly target exists
            has_quarterly_target = any([
                outcome.target_q1 is not None,
                outcome.target_q2 is not None,
                outcome.target_q3 is not None,
                outcome.target_q4 is not None
            ])
            if not has_quarterly_target:
                errors.append(f"{outcome_prefix} ('{outcome.description}') must have at least one quarterly target.")

        return (len(errors) == 0, errors)

    def can_approve_goal(self, approver_id: str, goal_id: str) -> Tuple[bool, str]:
        """
        Check if a person has permission to approve a goal

        Approval rules:
        - Executives can approve any goal
        - Direct manager can approve their reports' goals
        - Department heads can approve goals in their department

        Args:
            approver_id: Person attempting to approve
            goal_id: Goal to approve

        Returns:
            Tuple of (can_approve, reason_message)
        """
        approver = self.repo.get_person(approver_id)
        if not approver:
            return (False, "Approver not found")

        # Find the goal
        all_individual = self.repo.get_all_individual_goals()
        goal = next((g for g in all_individual if g.id == goal_id), None)
        if not goal:
            return (False, "Goal not found")

        goal_owner = self.repo.get_person(goal.person_id)
        if not goal_owner:
            return (False, "Goal owner not found")

        # Check approval permissions
        if approver.level == 'executive':
            return (True, "Executive can approve all goals")

        if approver.level == 'department_head':
            # Department heads can approve goals in their department
            if goal_owner.department_id == approver.department_id:
                return (True, "Department head can approve goals in their department")

        if goal_owner.manager_id == approver_id:
            return (True, "Direct manager can approve")

        return (False, "Only direct manager, department head, or executive can approve this goal")

    def check_goal_limit(self, person_id: str) -> Tuple[bool, int]:
        """
        Check if person has reached the 3-goal limit

        Args:
            person_id: Person to check

        Returns:
            Tuple of (can_create_more, current_active_count)
        """
        existing_goals = self.repo.get_individual_goals_by_person(person_id)
        active_goals = [g for g in existing_goals if g.status != 'archived']
        active_count = len(active_goals)

        can_create = active_count < 3
        return (can_create, active_count)

    def validate_why_length(self, why: str) -> Tuple[bool, str]:
        """
        Validate WHY statement length (3 sentences max, ~500 chars)

        Args:
            why: WHY statement to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not why or len(why.strip()) == 0:
            return (False, "WHY statement cannot be empty")

        if len(why) > 500:
            return (False, "WHY statement should be 3 sentences max (~500 characters)")

        # Count sentences (approximate - count periods)
        sentence_count = why.count('.') + why.count('!') + why.count('?')
        if sentence_count > 3:
            return (False, "WHY statement should be 3 sentences maximum")

        return (True, "")

    def validate_goal_length(self, goal: str) -> Tuple[bool, str]:
        """
        Validate GOAL statement length (~300 chars)

        Args:
            goal: GOAL statement to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not goal or len(goal.strip()) == 0:
            return (False, "GOAL statement cannot be empty")

        if len(goal) > 300:
            return (False, "GOAL statement should be concise (~300 characters)")

        return (True, "")

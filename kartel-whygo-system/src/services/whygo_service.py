"""
WhyGO Service - Business logic for retrieving and displaying WhyGOs

Handles dashboard data retrieval and rollup calculations.
"""

from typing import List, Optional, Dict
from ..repositories.interfaces import IWhygoRepository
from ..models.whygo import CompanyWhyGO, DepartmentWhyGO, IndividualWhyGO, Outcome


class WhygoService:
    """Service for retrieving and formatting WhyGO data"""

    def __init__(self, whygo_repo: IWhygoRepository):
        self.repo = whygo_repo

    def get_company_dashboard_data(self) -> dict:
        """
        Get all company goals with summary statistics.

        Returns:
            Dictionary with company goals and summary stats
        """
        goals = self.repo.get_all_company_goals()

        # Calculate summary statistics
        total_outcomes = sum(len(g.outcomes) for g in goals)
        outcomes_with_q1_data = sum(
            1 for g in goals for o in g.outcomes if o.actual_q1 is not None
        )

        # Calculate status distribution for Q1
        status_counts = {'+': 0, '~': 0, '-': 0, None: 0}
        for goal in goals:
            for outcome in goal.outcomes:
                status = outcome.status_q1
                status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'goals': goals,
            'summary': {
                'total_goals': len(goals),
                'total_outcomes': total_outcomes,
                'outcomes_tracked_q1': outcomes_with_q1_data,
                'q1_status': {
                    'on_pace': status_counts.get('+', 0),
                    'slightly_off': status_counts.get('~', 0),
                    'off_pace': status_counts.get('-', 0),
                    'not_recorded': status_counts.get(None, 0)
                }
            }
        }

    def get_department_dashboard_data(self, dept_id: str) -> dict:
        """
        Get department goals with summary statistics.

        Args:
            dept_id: Department ID (e.g., 'dept_sales')

        Returns:
            Dictionary with department goals and summary
        """
        goals = self.repo.get_department_goals_by_department(dept_id)

        if not goals:
            return {
                'department_id': dept_id,
                'goals': [],
                'summary': {}
            }

        # Calculate summary
        total_outcomes = sum(len(g.outcomes) for g in goals)
        outcomes_with_q1_data = sum(
            1 for g in goals for o in g.outcomes if o.actual_q1 is not None
        )

        # Calculate status distribution for Q1
        status_counts = {'+': 0, '~': 0, '-': 0, None: 0}
        for goal in goals:
            for outcome in goal.outcomes:
                status = outcome.status_q1
                status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'department_id': dept_id,
            'goals': goals,
            'summary': {
                'total_goals': len(goals),
                'total_outcomes': total_outcomes,
                'outcomes_tracked_q1': outcomes_with_q1_data,
                'q1_status': {
                    'on_pace': status_counts.get('+', 0),
                    'slightly_off': status_counts.get('~', 0),
                    'off_pace': status_counts.get('-', 0),
                    'not_recorded': status_counts.get(None, 0)
                }
            }
        }

    def get_outcome_details(self, outcome_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific outcome.

        Args:
            outcome_id: Outcome ID (e.g., 'cg_1_o1')

        Returns:
            Dictionary with outcome details or None if not found
        """
        outcome = self.repo.get_outcome(outcome_id)
        if not outcome:
            return None

        return {
            'id': outcome.id,
            'description': outcome.description,
            'metric_type': outcome.metric_type,
            'owner_id': outcome.owner_id,
            'annual_target': outcome.target_annual,
            'quarters': {
                'Q1': {
                    'target': outcome.target_q1,
                    'actual': outcome.actual_q1,
                    'status': outcome.status_q1,
                    'percentage': self._calculate_percentage(outcome.target_q1, outcome.actual_q1, outcome.metric_type)
                },
                'Q2': {
                    'target': outcome.target_q2,
                    'actual': outcome.actual_q2,
                    'status': outcome.status_q2,
                    'percentage': self._calculate_percentage(outcome.target_q2, outcome.actual_q2, outcome.metric_type)
                },
                'Q3': {
                    'target': outcome.target_q3,
                    'actual': outcome.actual_q3,
                    'status': outcome.status_q3,
                    'percentage': self._calculate_percentage(outcome.target_q3, outcome.actual_q3, outcome.metric_type)
                },
                'Q4': {
                    'target': outcome.target_q4,
                    'actual': outcome.actual_q4,
                    'status': outcome.status_q4,
                    'percentage': self._calculate_percentage(outcome.target_q4, outcome.actual_q4, outcome.metric_type)
                }
            }
        }

    def _calculate_percentage(self, target, actual, metric_type: str) -> Optional[float]:
        """Calculate percentage completion for numeric metrics"""
        if metric_type not in ['number', 'currency', 'percentage']:
            return None

        if target is None or actual is None:
            return None

        try:
            target_val = float(target)
            actual_val = float(actual)

            if target_val == 0:
                return 100.0 if actual_val == 0 else None

            return round((actual_val / target_val) * 100, 1)
        except (ValueError, TypeError):
            return None

    def get_all_outcomes_for_person(self, person_id: str) -> List[Outcome]:
        """
        Get all outcomes owned by a specific person across all goals.

        Args:
            person_id: Person ID (e.g., 'person_ben_kusin')

        Returns:
            List of outcomes owned by this person
        """
        outcomes = []

        # Search company goals
        for goal in self.repo.get_all_company_goals():
            for outcome in goal.outcomes:
                if outcome.owner_id == person_id:
                    outcomes.append(outcome)

        # Search department goals
        for goal in self.repo.get_all_department_goals():
            for outcome in goal.outcomes:
                if outcome.owner_id == person_id:
                    outcomes.append(outcome)

        # Search individual goals
        for goal in self.repo.get_all_individual_goals():
            for outcome in goal.outcomes:
                if outcome.owner_id == person_id:
                    outcomes.append(outcome)

        return outcomes

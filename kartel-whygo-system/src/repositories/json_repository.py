"""
JSON file implementation of repository interfaces

Loads all data into memory on init, operates on in-memory objects,
and writes back to JSON files on save_all().
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from .interfaces import IWhygoRepository, IProgressRepository
from ..models.whygo import (
    CompanyWhyGO,
    DepartmentWhyGO,
    IndividualWhyGO,
    Outcome,
    ProgressUpdate,
    whygo_to_dict,
    progress_update_to_dict
)


class JsonWhygoRepository(IWhygoRepository):
    """JSON file-based implementation of WhyGO repository"""

    def __init__(self, data_dir: str = "data/"):
        self.data_dir = Path(data_dir)
        self._company_goals = self._load_company_goals()
        self._department_goals = self._load_department_goals()
        self._individual_goals = self._load_individual_goals()

    def _load_company_goals(self) -> List[CompanyWhyGO]:
        """Load company WhyGOs from JSON"""
        file_path = self.data_dir / "company_whygos.json"
        with open(file_path, 'r') as f:
            data = json.load(f)

        goals = []
        for goal_data in data.get("company_goals", []):
            # Parse outcomes
            outcomes = []
            for outcome_data in goal_data.get("outcomes", []):
                outcome = Outcome(
                    id=outcome_data["id"],
                    goal_id=outcome_data["goal_id"],
                    description=outcome_data["description"],
                    metric_type=outcome_data["metric_type"],
                    owner_id=outcome_data["owner_id"],
                    target_annual=outcome_data["target_annual"],
                    target_q1=outcome_data.get("target_q1"),
                    target_q2=outcome_data.get("target_q2"),
                    target_q3=outcome_data.get("target_q3"),
                    target_q4=outcome_data.get("target_q4"),
                    actual_q1=outcome_data.get("actual_q1"),
                    actual_q2=outcome_data.get("actual_q2"),
                    actual_q3=outcome_data.get("actual_q3"),
                    actual_q4=outcome_data.get("actual_q4"),
                    status_q1=outcome_data.get("status_q1"),
                    status_q2=outcome_data.get("status_q2"),
                    status_q3=outcome_data.get("status_q3"),
                    status_q4=outcome_data.get("status_q4")
                )
                outcomes.append(outcome)

            # Parse company WhyGO
            goal = CompanyWhyGO(
                id=goal_data["id"],
                level=goal_data["level"],
                why=goal_data.get("why", ""),
                goal=goal_data.get("goal", ""),
                status=goal_data.get("status", "draft"),
                owner_id=goal_data.get("owner_id", ""),
                fiscal_year=goal_data.get("fiscal_year", 2026),
                outcomes=outcomes,
                created_at=goal_data.get("created_at", ""),
                updated_at=goal_data.get("updated_at", "")
            )
            goals.append(goal)

        return goals

    def _load_department_goals(self) -> List[DepartmentWhyGO]:
        """Load department WhyGOs from JSON"""
        file_path = self.data_dir / "department_goals.json"
        with open(file_path, 'r') as f:
            data = json.load(f)

        goals = []
        for goal_data in data.get("department_goals", []):
            # Parse outcomes
            outcomes = []
            for outcome_data in goal_data.get("outcomes", []):
                outcome = Outcome(
                    id=outcome_data["id"],
                    goal_id=outcome_data["goal_id"],
                    description=outcome_data["description"],
                    metric_type=outcome_data["metric_type"],
                    owner_id=outcome_data["owner_id"],
                    target_annual=outcome_data["target_annual"],
                    target_q1=outcome_data.get("target_q1"),
                    target_q2=outcome_data.get("target_q2"),
                    target_q3=outcome_data.get("target_q3"),
                    target_q4=outcome_data.get("target_q4"),
                    actual_q1=outcome_data.get("actual_q1"),
                    actual_q2=outcome_data.get("actual_q2"),
                    actual_q3=outcome_data.get("actual_q3"),
                    actual_q4=outcome_data.get("actual_q4"),
                    status_q1=outcome_data.get("status_q1"),
                    status_q2=outcome_data.get("status_q2"),
                    status_q3=outcome_data.get("status_q3"),
                    status_q4=outcome_data.get("status_q4")
                )
                outcomes.append(outcome)

            # Parse department WhyGO
            goal = DepartmentWhyGO(
                id=goal_data["id"],
                level=goal_data["level"],
                department_id=goal_data["department_id"],
                parent_goal_ids=goal_data.get("parent_goal_ids", []),
                why=goal_data.get("why", ""),
                goal=goal_data.get("goal", ""),
                status=goal_data.get("status", "draft"),
                approved_by=goal_data.get("approved_by"),
                fiscal_year=goal_data.get("fiscal_year", 2026),
                outcomes=outcomes,
                created_at=goal_data.get("created_at", ""),
                updated_at=goal_data.get("updated_at", "")
            )
            goals.append(goal)

        return goals

    def _load_individual_goals(self) -> List[IndividualWhyGO]:
        """Load individual WhyGOs from JSON"""
        file_path = self.data_dir / "individual_goals.json"
        with open(file_path, 'r') as f:
            data = json.load(f)

        goals = []
        for goal_data in data.get("individual_goals", []):
            # Parse outcomes
            outcomes = []
            for outcome_data in goal_data.get("outcomes", []):
                outcome = Outcome(
                    id=outcome_data["id"],
                    goal_id=outcome_data["goal_id"],
                    description=outcome_data["description"],
                    metric_type=outcome_data["metric_type"],
                    owner_id=outcome_data["owner_id"],
                    target_annual=outcome_data["target_annual"],
                    target_q1=outcome_data.get("target_q1"),
                    target_q2=outcome_data.get("target_q2"),
                    target_q3=outcome_data.get("target_q3"),
                    target_q4=outcome_data.get("target_q4"),
                    actual_q1=outcome_data.get("actual_q1"),
                    actual_q2=outcome_data.get("actual_q2"),
                    actual_q3=outcome_data.get("actual_q3"),
                    actual_q4=outcome_data.get("actual_q4"),
                    status_q1=outcome_data.get("status_q1"),
                    status_q2=outcome_data.get("status_q2"),
                    status_q3=outcome_data.get("status_q3"),
                    status_q4=outcome_data.get("status_q4")
                )
                outcomes.append(outcome)

            # Parse individual WhyGO
            goal = IndividualWhyGO(
                id=goal_data["id"],
                level=goal_data["level"],
                person_id=goal_data["person_id"],
                parent_goal_ids=goal_data.get("parent_goal_ids", []),
                why=goal_data.get("why", ""),
                goal=goal_data.get("goal", ""),
                status=goal_data.get("status", "draft"),
                approved_by=goal_data.get("approved_by"),
                fiscal_year=goal_data.get("fiscal_year", 2026),
                outcomes=outcomes,
                created_at=goal_data.get("created_at", ""),
                updated_at=goal_data.get("updated_at", "")
            )
            goals.append(goal)

        return goals

    def get_all_company_goals(self) -> List[CompanyWhyGO]:
        """Get all company-level WhyGOs"""
        return self._company_goals

    def get_company_goal(self, goal_id: str) -> Optional[CompanyWhyGO]:
        """Get a specific company WhyGO by ID"""
        for goal in self._company_goals:
            if goal.id == goal_id:
                return goal
        return None

    def get_all_department_goals(self) -> List[DepartmentWhyGO]:
        """Get all department-level WhyGOs"""
        return self._department_goals

    def get_department_goals_by_department(self, dept_id: str) -> List[DepartmentWhyGO]:
        """Get all WhyGOs for a specific department"""
        return [g for g in self._department_goals if g.department_id == dept_id]

    def get_all_individual_goals(self) -> List[IndividualWhyGO]:
        """Get all individual-level WhyGOs"""
        return self._individual_goals

    def get_individual_goals_by_person(self, person_id: str) -> List[IndividualWhyGO]:
        """Get all WhyGOs for a specific person"""
        return [g for g in self._individual_goals if g.person_id == person_id]

    def get_outcome(self, outcome_id: str) -> Optional[Outcome]:
        """Find an outcome by ID across all goals"""
        # Search company goals
        for goal in self._company_goals:
            for outcome in goal.outcomes:
                if outcome.id == outcome_id:
                    return outcome

        # Search department goals
        for goal in self._department_goals:
            for outcome in goal.outcomes:
                if outcome.id == outcome_id:
                    return outcome

        # Search individual goals
        for goal in self._individual_goals:
            for outcome in goal.outcomes:
                if outcome.id == outcome_id:
                    return outcome

        return None

    def update_outcome(self, outcome: Outcome) -> bool:
        """Update an outcome (in-memory only, call save_all() to persist)"""
        # Find and update the outcome in the appropriate goal
        # The outcome object is already updated in memory since Python passes by reference
        # We just need to update the updated_at timestamp on the parent goal

        # Search company goals
        for goal in self._company_goals:
            for idx, existing_outcome in enumerate(goal.outcomes):
                if existing_outcome.id == outcome.id:
                    goal.outcomes[idx] = outcome
                    goal.updated_at = datetime.now().isoformat()
                    return True

        # Search department goals
        for goal in self._department_goals:
            for idx, existing_outcome in enumerate(goal.outcomes):
                if existing_outcome.id == outcome.id:
                    goal.outcomes[idx] = outcome
                    goal.updated_at = datetime.now().isoformat()
                    return True

        # Search individual goals
        for goal in self._individual_goals:
            for idx, existing_outcome in enumerate(goal.outcomes):
                if existing_outcome.id == outcome.id:
                    goal.outcomes[idx] = outcome
                    goal.updated_at = datetime.now().isoformat()
                    return True

        return False

    def save_all(self) -> bool:
        """Write all data back to JSON files"""
        try:
            # Save company goals
            company_file = self.data_dir / "company_whygos.json"
            with open(company_file, 'r') as f:
                company_data = json.load(f)

            company_data["company_goals"] = [whygo_to_dict(g) for g in self._company_goals]
            company_data["metadata"]["last_updated"] = datetime.now().isoformat()

            with open(company_file, 'w') as f:
                json.dump(company_data, f, indent=2)

            # Save department goals
            dept_file = self.data_dir / "department_goals.json"
            with open(dept_file, 'r') as f:
                dept_data = json.load(f)

            dept_data["department_goals"] = [whygo_to_dict(g) for g in self._department_goals]
            dept_data["metadata"]["last_updated"] = datetime.now().isoformat()

            with open(dept_file, 'w') as f:
                json.dump(dept_data, f, indent=2)

            # Save individual goals
            indiv_file = self.data_dir / "individual_goals.json"
            with open(indiv_file, 'r') as f:
                indiv_data = json.load(f)

            indiv_data["individual_goals"] = [whygo_to_dict(g) for g in self._individual_goals]
            indiv_data["metadata"]["last_updated"] = datetime.now().isoformat()

            with open(indiv_file, 'w') as f:
                json.dump(indiv_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving WhyGO data: {e}")
            return False


class JsonProgressRepository(IProgressRepository):
    """JSON file-based implementation of progress update repository"""

    def __init__(self, data_dir: str = "data/"):
        self.data_dir = Path(data_dir)
        self._updates = self._load_updates()

    def _load_updates(self) -> List[ProgressUpdate]:
        """Load progress updates from JSON"""
        file_path = self.data_dir / "progress_updates.json"
        with open(file_path, 'r') as f:
            data = json.load(f)

        updates = []
        for update_data in data.get("progress_updates", []):
            update = ProgressUpdate(
                id=update_data["id"],
                outcome_id=update_data["outcome_id"],
                quarter=update_data["quarter"],
                actual_value=update_data.get("actual_value"),
                status=update_data.get("status"),
                notes=update_data.get("notes"),
                blocker=update_data.get("blocker"),
                recorded_by=update_data.get("recorded_by", ""),
                recorded_at=update_data.get("recorded_at", "")
            )
            updates.append(update)

        return updates

    def record_progress(self, update: ProgressUpdate) -> bool:
        """Record a progress update (in-memory, call save_all() to persist)"""
        self._updates.append(update)
        return True

    def get_updates_for_outcome(self, outcome_id: str) -> List[ProgressUpdate]:
        """Get all progress updates for a specific outcome"""
        return [u for u in self._updates if u.outcome_id == outcome_id]

    def get_all_updates(self) -> List[ProgressUpdate]:
        """Get all progress updates"""
        return self._updates

    def save_all(self) -> bool:
        """Write all progress updates back to JSON"""
        try:
            file_path = self.data_dir / "progress_updates.json"
            with open(file_path, 'r') as f:
                data = json.load(f)

            data["progress_updates"] = [progress_update_to_dict(u) for u in self._updates]
            data["metadata"]["last_updated"] = datetime.now().isoformat()

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving progress updates: {e}")
            return False

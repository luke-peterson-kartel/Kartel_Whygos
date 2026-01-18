"""
Progress Service - Business logic for tracking progress

Handles recording actuals, calculating status, and managing progress updates.
"""

from datetime import datetime
from typing import Literal, Union, Optional
from ..repositories.interfaces import IWhygoRepository, IProgressRepository
from ..models.whygo import Outcome, ProgressUpdate
from ..utils.id_generator import generate_progress_update_id


class ProgressService:
    """Service for managing progress tracking and status calculation"""

    def __init__(self, whygo_repo: IWhygoRepository, progress_repo: IProgressRepository):
        self.whygo_repo = whygo_repo
        self.progress_repo = progress_repo

    def record_actual(
        self,
        outcome_id: str,
        quarter: Literal['Q1', 'Q2', 'Q3', 'Q4'],
        actual_value: Union[int, float, str],
        recorded_by: str,
        notes: Optional[str] = None,
        blocker: Optional[str] = None
    ) -> bool:
        """
        Record actual value for an outcome in a quarter.
        Automatically calculates and sets status.

        Args:
            outcome_id: ID of the outcome to update
            quarter: Quarter ('Q1', 'Q2', 'Q3', 'Q4')
            actual_value: The actual value achieved
            recorded_by: Person ID of who is recording this
            notes: Optional notes about the progress
            blocker: Optional blocker description if off-track

        Returns:
            True if successful, False otherwise
        """
        # Get the outcome
        outcome = self.whygo_repo.get_outcome(outcome_id)
        if not outcome:
            print(f"❌ Outcome not found: {outcome_id}")
            return False

        # Set actual value
        quarter_lower = quarter.lower()
        setattr(outcome, f'actual_{quarter_lower}', actual_value)

        # Calculate status
        status = self._calculate_status(outcome, quarter)
        setattr(outcome, f'status_{quarter_lower}', status)

        # Update outcome in repository
        self.whygo_repo.update_outcome(outcome)

        # Create progress update record
        update = ProgressUpdate(
            id=generate_progress_update_id(outcome_id, quarter),
            outcome_id=outcome_id,
            quarter=quarter,
            actual_value=actual_value,
            status=status,
            notes=notes,
            blocker=blocker,
            recorded_by=recorded_by,
            recorded_at=datetime.now().isoformat()
        )

        # Record progress update
        self.progress_repo.record_progress(update)

        # Persist changes
        whygo_saved = self.whygo_repo.save_all()
        progress_saved = self.progress_repo.save_all()

        return whygo_saved and progress_saved

    def _calculate_status(
        self,
        outcome: Outcome,
        quarter: str
    ) -> Optional[Literal['+', '~', '-']]:
        """
        Calculate status based on actual vs target.

        Rules:
        - Number/Currency/Percentage:
          - [+] if actual >= target (100%+)
          - [~] if actual >= 80% of target
          - [-] if actual < 80%
        - Milestone/Boolean:
          - [+] if actual matches target
          - [-] otherwise

        Args:
            outcome: The outcome to calculate status for
            quarter: Quarter string ('Q1', 'Q2', 'Q3', 'Q4')

        Returns:
            Status symbol ('+', '~', '-') or None if can't calculate
        """
        quarter_lower = quarter.lower()
        target = getattr(outcome, f'target_{quarter_lower}')
        actual = getattr(outcome, f'actual_{quarter_lower}')

        # Can't calculate if either is missing
        if target is None or actual is None:
            return None

        metric_type = outcome.metric_type

        # Number-based metrics (number, currency, percentage)
        if metric_type in ['number', 'currency', 'percentage']:
            try:
                # Convert to float for calculation
                target_val = float(target) if not isinstance(target, (int, float)) else target
                actual_val = float(actual) if not isinstance(actual, (int, float)) else actual

                if target_val == 0:
                    # Avoid division by zero - if target is 0 and actual is 0, that's on track
                    return '+' if actual_val == 0 else '-'

                percentage = (actual_val / target_val) * 100

                if percentage >= 100:
                    return '+'
                elif percentage >= 80:
                    return '~'
                else:
                    return '-'
            except (ValueError, TypeError):
                print(f"⚠️  Could not convert values to numbers for calculation: target={target}, actual={actual}")
                return '-'

        # Milestone/Boolean metrics (exact match required)
        elif metric_type in ['milestone', 'boolean']:
            # Convert both to strings for comparison (handles case differences)
            target_str = str(target).strip().lower()
            actual_str = str(actual).strip().lower()
            return '+' if actual_str == target_str else '-'

        # Unknown metric type
        return '-'

    def get_outcome_progress_history(self, outcome_id: str) -> dict:
        """
        Get complete progress history for an outcome.

        Returns:
            Dictionary with outcome and all its progress updates
        """
        outcome = self.whygo_repo.get_outcome(outcome_id)
        if not outcome:
            return {}

        updates = self.progress_repo.get_updates_for_outcome(outcome_id)

        return {
            'outcome': outcome,
            'updates': updates,
            'quarterly_status': {
                'Q1': {
                    'target': outcome.target_q1,
                    'actual': outcome.actual_q1,
                    'status': outcome.status_q1
                },
                'Q2': {
                    'target': outcome.target_q2,
                    'actual': outcome.actual_q2,
                    'status': outcome.status_q2
                },
                'Q3': {
                    'target': outcome.target_q3,
                    'actual': outcome.actual_q3,
                    'status': outcome.status_q3
                },
                'Q4': {
                    'target': outcome.target_q4,
                    'actual': outcome.actual_q4,
                    'status': outcome.status_q4
                }
            }
        }

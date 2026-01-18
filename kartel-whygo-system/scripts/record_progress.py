#!/usr/bin/env python3
"""
CLI tool to record progress updates

Usage:
  python scripts/record_progress.py cg_1_o1 Q1 5 --person person_ben_kusin
  python scripts/record_progress.py cg_4_o1 Q1 "MVP" --person person_niels --notes "Launched ahead of schedule"
  python scripts/record_progress.py cg_2_o1 Q1 35 --person person_luke_peterson --blocker "Workflow delays"

Examples:
  # Record numeric actual
  python scripts/record_progress.py cg_1_o1 Q1 5 --person person_ben_kusin --notes "Signed 5 clients in Q1"

  # Record milestone actual
  python scripts/record_progress.py cg_4_o1 Q1 "MVP" --person person_niels

  # Record with blocker
  python scripts/record_progress.py cg_2_o1 Q1 35 --person person_luke_peterson --blocker "Workflow delays impacting timeline"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories.json_repository import JsonWhygoRepository, JsonProgressRepository
from src.services.progress_service import ProgressService


def parse_actual_value(value_str: str):
    """
    Convert string input to appropriate type.

    Tries to convert to number if possible, otherwise keeps as string.
    """
    # Try to parse as number
    try:
        # Try integer first
        if '.' not in value_str:
            return int(value_str)
        # Then float
        return float(value_str)
    except ValueError:
        # Keep as string (for milestones like "MVP", "Live", etc.)
        return value_str


def main():
    parser = argparse.ArgumentParser(
        description='Record progress for an outcome',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record numeric actual
  python scripts/record_progress.py cg_1_o1 Q1 5 --person person_ben_kusin --notes "Signed 5 clients"

  # Record milestone actual
  python scripts/record_progress.py cg_4_o1 Q1 "MVP" --person person_niels

  # Record with blocker
  python scripts/record_progress.py cg_2_o1 Q1 35 --person person_luke_peterson --blocker "Delays"
        """
    )

    parser.add_argument('outcome_id', help='Outcome ID (e.g., cg_1_o1)')
    parser.add_argument('quarter', choices=['Q1', 'Q2', 'Q3', 'Q4'], help='Quarter')
    parser.add_argument('actual', help='Actual value achieved')
    parser.add_argument('--person', required=True, help='Person ID recording update (e.g., person_ben_kusin)')
    parser.add_argument('--notes', help='Optional notes about the progress')
    parser.add_argument('--blocker', help='Optional blocker description if off-track')

    args = parser.parse_args()

    # Initialize repositories and service
    whygo_repo = JsonWhygoRepository()
    progress_repo = JsonProgressRepository()
    service = ProgressService(whygo_repo, progress_repo)

    # Convert actual to appropriate type
    actual = parse_actual_value(args.actual)

    print(f"\n🎯 Recording progress for {args.outcome_id}")
    print(f"   Quarter: {args.quarter}")
    print(f"   Actual: {actual}")
    print(f"   Recorded by: {args.person}")
    if args.notes:
        print(f"   Notes: {args.notes}")
    if args.blocker:
        print(f"   ⚠️  Blocker: {args.blocker}")

    # Record progress
    success = service.record_actual(
        outcome_id=args.outcome_id,
        quarter=args.quarter,
        actual_value=actual,
        recorded_by=args.person,
        notes=args.notes,
        blocker=args.blocker
    )

    if success:
        # Get the outcome to display status
        outcome = whygo_repo.get_outcome(args.outcome_id)
        if outcome:
            quarter_lower = args.quarter.lower()
            status = getattr(outcome, f'status_{quarter_lower}')
            target = getattr(outcome, f'target_{quarter_lower}')

            print(f"\n✅ Progress recorded successfully!")
            print(f"   Target: {target}")
            print(f"   Actual: {actual}")

            # Display status with emoji
            if status == '+':
                print(f"   Status: [+] On pace! 🎉")
            elif status == '~':
                print(f"   Status: [~] Slightly off pace")
            elif status == '-':
                print(f"   Status: [-] Off pace ⚠️")
            else:
                print(f"   Status: Not calculated")

            print(f"\n📁 Updated files:")
            print(f"   - data/company_whygos.json (or department/individual)")
            print(f"   - data/progress_updates.json")
        else:
            print(f"\n✅ Progress recorded but could not retrieve outcome for status display")
    else:
        print(f"\n❌ Failed to record progress")
        print(f"   Check that the outcome ID exists: {args.outcome_id}")
        sys.exit(1)


if __name__ == "__main__":
    main()

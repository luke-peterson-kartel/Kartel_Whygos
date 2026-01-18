#!/usr/bin/env python3
"""
Display WhyGO dashboard

Usage:
  python scripts/view_dashboard.py company
  python scripts/view_dashboard.py department sales
  python scripts/view_dashboard.py outcome cg_1_o1
  python scripts/view_dashboard.py person person_ben_kusin
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.repositories.json_repository import JsonWhygoRepository
from src.services.whygo_service import WhygoService


def format_status(status):
    """Format status with emoji"""
    if status == '+':
        return '[+] On pace 🎉'
    elif status == '~':
        return '[~] Slightly off'
    elif status == '-':
        return '[-] Off pace ⚠️'
    else:
        return '[ ] Not recorded'


def display_company_dashboard(service: WhygoService):
    """Display company-level dashboard"""
    data = service.get_company_dashboard_data()

    print("\n" + "=" * 80)
    print("📋 COMPANY WHYGOS - 2026")
    print("=" * 80)

    summary = data['summary']
    print(f"\n📊 Summary:")
    print(f"   Total Goals: {summary['total_goals']}")
    print(f"   Total Outcomes: {summary['total_outcomes']}")
    print(f"   Q1 Tracked: {summary['outcomes_tracked_q1']}/{summary['total_outcomes']}")
    print(f"\n   Q1 Status:")
    q1_status = summary['q1_status']
    print(f"      [+] On pace: {q1_status['on_pace']}")
    print(f"      [~] Slightly off: {q1_status['slightly_off']}")
    print(f"      [-] Off pace: {q1_status['off_pace']}")
    print(f"      [ ] Not recorded: {q1_status['not_recorded']}")

    print("\n" + "-" * 80)

    for goal in data['goals']:
        print(f"\n🎯 {goal.id.upper()}: {goal.goal[:60]}...")
        print(f"   Status: {goal.status}")
        print(f"   Outcomes: {len(goal.outcomes)}")

        for outcome in goal.outcomes:
            status_str = format_status(outcome.status_q1)
            target = f"Target: {outcome.target_q1}" if outcome.target_q1 else "No target"
            actual = f"Actual: {outcome.actual_q1}" if outcome.actual_q1 is not None else "Not recorded"

            print(f"\n   • {outcome.description}")
            print(f"     {status_str}")
            print(f"     Q1: {target} | {actual}")

    print("\n" + "=" * 80 + "\n")


def display_department_dashboard(service: WhygoService, dept_id: str):
    """Display department-level dashboard"""
    data = service.get_department_dashboard_data(dept_id)

    if not data['goals']:
        print(f"\n❌ No goals found for department: {dept_id}")
        return

    print("\n" + "=" * 80)
    print(f"🏢 DEPARTMENT WHYGOS - {dept_id.upper()}")
    print("=" * 80)

    summary = data['summary']
    print(f"\n📊 Summary:")
    print(f"   Total Goals: {summary['total_goals']}")
    print(f"   Total Outcomes: {summary['total_outcomes']}")
    print(f"   Q1 Tracked: {summary['outcomes_tracked_q1']}/{summary['total_outcomes']}")

    print("\n" + "-" * 80)

    for goal in data['goals']:
        print(f"\n🎯 {goal.id.upper()}: {goal.goal[:60]}...")
        print(f"   Ladders to: {', '.join(goal.parent_goal_ids)}")
        print(f"   Outcomes: {len(goal.outcomes)}")

        for outcome in goal.outcomes:
            status_str = format_status(outcome.status_q1)
            target = f"Target: {outcome.target_q1}" if outcome.target_q1 else "No target"
            actual = f"Actual: {outcome.actual_q1}" if outcome.actual_q1 is not None else "Not recorded"

            print(f"\n   • {outcome.description}")
            print(f"     {status_str}")
            print(f"     Q1: {target} | {actual}")
            print(f"     Owner: {outcome.owner_id}")

    print("\n" + "=" * 80 + "\n")


def display_outcome_details(service: WhygoService, outcome_id: str):
    """Display detailed view of a single outcome"""
    data = service.get_outcome_details(outcome_id)

    if not data:
        print(f"\n❌ Outcome not found: {outcome_id}")
        return

    print("\n" + "=" * 80)
    print(f"📈 OUTCOME DETAILS - {outcome_id}")
    print("=" * 80)

    print(f"\nDescription: {data['description']}")
    print(f"Type: {data['metric_type']}")
    print(f"Owner: {data['owner_id']}")
    print(f"Annual Target: {data['annual_target']}")

    print("\n" + "-" * 80)
    print("Quarterly Progress:")
    print("-" * 80)

    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        q_data = data['quarters'][quarter]
        target = q_data['target']
        actual = q_data['actual']
        status = q_data['status']
        percentage = q_data['percentage']

        status_str = format_status(status)

        print(f"\n{quarter}:")
        print(f"  Target:  {target if target is not None else 'N/A'}")
        print(f"  Actual:  {actual if actual is not None else 'Not recorded'}")
        if percentage is not None:
            print(f"  Progress: {percentage}%")
        print(f"  Status:  {status_str}")

    print("\n" + "=" * 80 + "\n")


def display_person_outcomes(service: WhygoService, person_id: str):
    """Display all outcomes owned by a person"""
    outcomes = service.get_all_outcomes_for_person(person_id)

    if not outcomes:
        print(f"\n❌ No outcomes found for person: {person_id}")
        return

    print("\n" + "=" * 80)
    print(f"👤 OUTCOMES FOR {person_id.upper()}")
    print("=" * 80)

    print(f"\nTotal outcomes owned: {len(outcomes)}")

    # Group by status
    on_pace = sum(1 for o in outcomes if o.status_q1 == '+')
    slightly_off = sum(1 for o in outcomes if o.status_q1 == '~')
    off_pace = sum(1 for o in outcomes if o.status_q1 == '-')
    not_recorded = sum(1 for o in outcomes if o.status_q1 is None)

    print(f"\nQ1 Status:")
    print(f"  [+] On pace: {on_pace}")
    print(f"  [~] Slightly off: {slightly_off}")
    print(f"  [-] Off pace: {off_pace}")
    print(f"  [ ] Not recorded: {not_recorded}")

    print("\n" + "-" * 80)

    for outcome in outcomes:
        status_str = format_status(outcome.status_q1)
        target = f"Target: {outcome.target_q1}" if outcome.target_q1 else "No target"
        actual = f"Actual: {outcome.actual_q1}" if outcome.actual_q1 is not None else "Not recorded"

        print(f"\n• {outcome.id}: {outcome.description}")
        print(f"  {status_str}")
        print(f"  Q1: {target} | {actual}")

    print("\n" + "=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='View WhyGO dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/view_dashboard.py company
  python scripts/view_dashboard.py department dept_sales
  python scripts/view_dashboard.py outcome cg_1_o1
  python scripts/view_dashboard.py person person_ben_kusin
        """
    )

    parser.add_argument('view_type', choices=['company', 'department', 'outcome', 'person'],
                       help='Type of dashboard to view')
    parser.add_argument('identifier', nargs='?',
                       help='ID for department/outcome/person (required for those view types)')

    args = parser.parse_args()

    # Validate identifier for views that need it
    if args.view_type in ['department', 'outcome', 'person'] and not args.identifier:
        print(f"❌ Error: '{args.view_type}' view requires an identifier")
        print(f"   Example: python scripts/view_dashboard.py {args.view_type} <id>")
        sys.exit(1)

    # Initialize repository and service
    whygo_repo = JsonWhygoRepository()
    service = WhygoService(whygo_repo)

    # Display appropriate dashboard
    if args.view_type == 'company':
        display_company_dashboard(service)
    elif args.view_type == 'department':
        display_department_dashboard(service, args.identifier)
    elif args.view_type == 'outcome':
        display_outcome_details(service, args.identifier)
    elif args.view_type == 'person':
        display_person_outcomes(service, args.identifier)


if __name__ == "__main__":
    main()

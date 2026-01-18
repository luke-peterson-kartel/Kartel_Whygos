#!/usr/bin/env python3
"""
Verify imported WhyGO data

Quick script to display imported data in readable format
"""

import json
from pathlib import Path


def main():
    data_dir = Path(__file__).parent.parent / "data"

    print("=" * 80)
    print("Kartel WhyGO Data Verification")
    print("=" * 80)
    print()

    # Company WhyGOs
    print("📋 COMPANY WHYGOS (4 goals)")
    print("-" * 80)

    with open(data_dir / "company_whygos.json") as f:
        company_data = json.load(f)

    for goal in company_data["company_goals"]:
        print(f"\n{goal['id'].upper()}: {goal['goal'][:60]}...")
        print(f"   Status: {goal['status']}")
        print(f"   Outcomes: {len(goal['outcomes'])}")

    print("\n" + "=" * 80)
    print()

    # Department WhyGOs
    print("🏢 DEPARTMENT WHYGOS (14 goals across 5 departments)")
    print("-" * 80)

    with open(data_dir / "department_goals.json") as f:
        dept_data = json.load(f)

    # Group by department
    by_dept = {}
    for goal in dept_data["department_goals"]:
        dept_id = goal["department_id"]
        if dept_id not in by_dept:
            by_dept[dept_id] = []
        by_dept[dept_id].append(goal)

    for dept_id, goals in by_dept.items():
        print(f"\n{dept_id.upper().replace('DEPT_', '')}:")
        for goal in goals:
            ladders = ", ".join(goal["parent_goal_ids"])
            print(f"  • {goal['id']} → [{ladders}] ({len(goal['outcomes'])} outcomes)")

    print("\n" + "=" * 80)
    print()

    # Alignment check
    print("🔗 ALIGNMENT VERIFICATION")
    print("-" * 80)

    # Check that all department goals reference valid company goals
    company_goal_ids = {g["id"] for g in company_data["company_goals"]}

    alignment_ok = True
    for goal in dept_data["department_goals"]:
        for parent_id in goal["parent_goal_ids"]:
            if parent_id not in company_goal_ids:
                print(f"⚠️  {goal['id']} references unknown company goal: {parent_id}")
                alignment_ok = False

    if alignment_ok:
        print("✅ All department goals properly ladder to company goals")

    print()

    # Outcome stats
    total_outcomes = sum(len(g["outcomes"]) for g in company_data["company_goals"])
    total_outcomes += sum(len(g["outcomes"]) for g in dept_data["department_goals"])

    with open(data_dir / "individual_goals.json") as f:
        indiv_data = json.load(f)
        total_outcomes += sum(len(g["outcomes"]) for g in indiv_data["individual_goals"])

    print("📊 SUMMARY STATISTICS")
    print("-" * 80)
    print(f"  Company Goals:     {len(company_data['company_goals'])}")
    print(f"  Department Goals:  {len(dept_data['department_goals'])}")
    print(f"  Individual Goals:  {len(indiv_data['individual_goals'])}")
    print(f"  Total Outcomes:    {total_outcomes}")

    with open(data_dir / "employees.json") as f:
        emp_data = json.load(f)
    print(f"  Employees:         {len(emp_data['employees'])}")

    with open(data_dir / "departments.json") as f:
        dept_ref_data = json.load(f)
    print(f"  Departments:       {len(dept_ref_data['departments'])}")

    print()
    print("=" * 80)
    print("✅ Data verification complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

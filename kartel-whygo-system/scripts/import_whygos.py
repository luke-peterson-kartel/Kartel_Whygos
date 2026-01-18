#!/usr/bin/env python3
"""
Import WhyGOs from Markdown Files

Main script to parse all WhyGO markdown files and generate JSON data files
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers.company_parser import parse_company_whygos
from src.parsers.department_parser import parse_department_whygos
from src.parsers.individual_parser import parse_individual_whygos
from src.parsers.reference_parser import parse_employees_from_reference, parse_departments
from src.models.whygo import whygo_to_dict, person_to_dict, department_to_dict


def main():
    print("=" * 60)
    print("Kartel WhyGO Import Script")
    print("=" * 60)
    print()

    # Set up paths
    base_dir = Path(__file__).parent.parent.parent
    company_md = base_dir / "Company WhyGos" / "Kartel_AI_Company_WhyGO__2026(Final).md"
    knowledge_dir = base_dir / "kartel-whygo-system" / "knowledge"
    data_dir = base_dir / "kartel-whygo-system" / "data"

    # Department files
    dept_files = {
        "Sales": base_dir / "Company WhyGos" / "Sales_Department_WhyGOs__2026(Final).md",
        "Production": base_dir / "Company WhyGos" / "Production_Department_WhyGOs_2026(Final).md",
        "Generative": base_dir / "Company WhyGos" / "Generative_Department_WhyGOs_2026(Final).md",
        "Community": base_dir / "Company WhyGos" / "Community_Department_WhyGOs_2026 (Final).md",
        "Platform": base_dir / "Company WhyGos" / "Platform_Department_WhyGOs__2026(Final).md"
    }

    # Individual files
    individual_files = {
        "Wayan Palmieri": base_dir / "INDIVIDUAL WHYGOS" / "Wayan_Individual_WhyGOs_2026_DRAFT.md"
    }

    # =============================================
    # Parse Company WhyGOs
    # =============================================
    print("📋 Parsing Company WhyGOs...")
    print(f"   File: {company_md.name}")

    try:
        company_whygos = parse_company_whygos(str(company_md))
        print(f"   ✓ Found {len(company_whygos)} Company WhyGOs")

        total_outcomes = sum(len(w.outcomes) for w in company_whygos)
        print(f"   ✓ Extracted {total_outcomes} outcomes with quarterly targets")
        print()

    except Exception as e:
        print(f"   ✗ Error: {e}")
        print()
        company_whygos = []

    # =============================================
    # Parse Department WhyGOs
    # =============================================
    print("🏢 Parsing Department WhyGOs...")

    all_dept_whygos = []
    dept_stats = {}

    for dept_name, dept_file in dept_files.items():
        print(f"   {dept_name}: ", end="")

        if not dept_file.exists():
            print(f"✗ File not found: {dept_file}")
            continue

        try:
            dept_whygos = parse_department_whygos(str(dept_file))
            all_dept_whygos.extend(dept_whygos)

            outcomes_count = sum(len(w.outcomes) for w in dept_whygos)
            dept_stats[dept_name] = {"goals": len(dept_whygos), "outcomes": outcomes_count}

            print(f"{len(dept_whygos)} WhyGOs, {outcomes_count} outcomes ✓")

        except Exception as e:
            print(f"✗ Error: {e}")

    print(f"   Total: {len(all_dept_whygos)} department goals")
    print()

    # =============================================
    # Parse Individual WhyGOs
    # =============================================
    print("👤 Parsing Individual WhyGOs...")

    all_individual_whygos = []

    for person_name, indiv_file in individual_files.items():
        print(f"   {person_name}: ", end="")

        if not indiv_file.exists():
            print(f"✗ File not found: {indiv_file}")
            continue

        try:
            indiv_whygos = parse_individual_whygos(str(indiv_file), person_name)
            all_individual_whygos.extend(indiv_whygos)

            outcomes_count = sum(len(w.outcomes) for w in indiv_whygos)
            print(f"{len(indiv_whygos)} WhyGOs, {outcomes_count} outcomes ✓")

        except Exception as e:
            print(f"✗ Error: {e}")

    print()

    # =============================================
    # Parse Reference Data
    # =============================================
    print("📚 Parsing Reference Data...")

    employee_ref_file = knowledge_dir / "EMPLOYEE_REFERENCE.md"

    try:
        employees = parse_employees_from_reference(str(employee_ref_file))
        print(f"   ✓ Loaded {len(employees)} employees")
    except Exception as e:
        print(f"   ✗ Error parsing employees: {e}")
        employees = []

    try:
        departments = parse_departments()
        print(f"   ✓ Loaded {len(departments)} departments")
    except Exception as e:
        print(f"   ✗ Error creating departments: {e}")
        departments = []

    print()

    # =============================================
    # Validation
    # =============================================
    print("🔍 Validating alignment...")

    # Check that department goals reference valid company goals
    company_goal_ids = {w.id for w in company_whygos}
    dept_parent_refs = []

    for dept_whygo in all_dept_whygos:
        for parent_id in dept_whygo.parent_goal_ids:
            if parent_id not in company_goal_ids:
                print(f"   ⚠ Warning: {dept_whygo.id} references unknown company goal {parent_id}")
            else:
                dept_parent_refs.append(parent_id)

    if dept_parent_refs:
        print(f"   ✓ All department goals ladder to company goals")

    # Check outcomes have owners
    all_outcomes = []
    for whygo in company_whygos + all_dept_whygos + all_individual_whygos:
        all_outcomes.extend(whygo.outcomes)

    outcomes_with_owners = sum(1 for o in all_outcomes if o.owner_id)
    print(f"   ✓ {outcomes_with_owners}/{len(all_outcomes)} outcomes have owners")

    # Check outcomes have quarterly targets
    outcomes_with_targets = sum(
        1 for o in all_outcomes
        if any([o.target_q1, o.target_q2, o.target_q3, o.target_q4])
    )
    print(f"   ✓ {outcomes_with_targets}/{len(all_outcomes)} outcomes have quarterly targets")

    print()

    # =============================================
    # Write JSON Files
    # =============================================
    print("💾 Writing JSON files...")

    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()

    # Company WhyGOs
    company_json = {
        "metadata": {
            "version": "1.0",
            "fiscal_year": 2026,
            "last_updated": timestamp,
            "source": "Imported from markdown files"
        },
        "company_goals": [whygo_to_dict(w) for w in company_whygos]
    }

    company_file = data_dir / "company_whygos.json"
    with open(company_file, 'w', encoding='utf-8') as f:
        json.dump(company_json, f, indent=2, ensure_ascii=False)

    print(f"   ✓ {company_file.name} ({len(company_whygos)} goals, {sum(len(w.outcomes) for w in company_whygos)} outcomes)")

    # Department WhyGOs
    dept_json = {
        "metadata": {
            "version": "1.0",
            "fiscal_year": 2026,
            "last_updated": timestamp,
            "source": "Imported from markdown files"
        },
        "department_goals": [whygo_to_dict(w) for w in all_dept_whygos]
    }

    dept_file = data_dir / "department_goals.json"
    with open(dept_file, 'w', encoding='utf-8') as f:
        json.dump(dept_json, f, indent=2, ensure_ascii=False)

    print(f"   ✓ {dept_file.name} ({len(all_dept_whygos)} goals, {sum(len(w.outcomes) for w in all_dept_whygos)} outcomes)")

    # Individual WhyGOs
    indiv_json = {
        "metadata": {
            "version": "1.0",
            "fiscal_year": 2026,
            "last_updated": timestamp,
            "source": "Imported from markdown files"
        },
        "individual_goals": [whygo_to_dict(w) for w in all_individual_whygos]
    }

    indiv_file = data_dir / "individual_goals.json"
    with open(indiv_file, 'w', encoding='utf-8') as f:
        json.dump(indiv_json, f, indent=2, ensure_ascii=False)

    print(f"   ✓ {indiv_file.name} ({len(all_individual_whygos)} goals, {sum(len(w.outcomes) for w in all_individual_whygos)} outcomes)")

    # Employees
    employees_json = {
        "metadata": {
            "version": "1.0",
            "last_updated": timestamp,
            "source": "EMPLOYEE_REFERENCE.md"
        },
        "employees": [person_to_dict(e) for e in employees]
    }

    emp_file = data_dir / "employees.json"
    with open(emp_file, 'w', encoding='utf-8') as f:
        json.dump(employees_json, f, indent=2, ensure_ascii=False)

    print(f"   ✓ {emp_file.name} ({len(employees)} employees)")

    # Departments
    dept_ref_json = {
        "metadata": {
            "version": "1.0",
            "last_updated": timestamp,
            "source": "DATA_STRUCTURES.md"
        },
        "departments": [department_to_dict(d) for d in departments]
    }

    dept_ref_file = data_dir / "departments.json"
    with open(dept_ref_file, 'w', encoding='utf-8') as f:
        json.dump(dept_ref_json, f, indent=2, ensure_ascii=False)

    print(f"   ✓ {dept_ref_file.name} ({len(departments)} departments)")

    print()
    print("=" * 60)
    print("✅ Import complete!")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  - Company Goals: {len(company_whygos)}")
    print(f"  - Department Goals: {len(all_dept_whygos)}")
    print(f"  - Individual Goals: {len(all_individual_whygos)}")
    print(f"  - Total Outcomes: {len(all_outcomes)}")
    print(f"  - Employees: {len(employees)}")
    print(f"  - Departments: {len(departments)}")
    print()


if __name__ == "__main__":
    main()
